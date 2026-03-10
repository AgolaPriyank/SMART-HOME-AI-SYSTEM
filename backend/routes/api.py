from flask import Blueprint, jsonify, request
from models import db, Device, SensorData, AutomationLog
import os
import sys

# Attempt to import ML predictor, handle graceful failure if not trained yet
try:
    from ml.predict import predict_device_state
    ML_AVAILABLE = True
except ImportError:
    ML_AVAILABLE = False

api_blueprint = Blueprint('api', __name__)

@api_blueprint.route('/sensors', methods=['POST'])
def receive_sensor_data():
    data = request.json
    
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400
        
    try:
        new_data = SensorData(
            temperature=data.get('temperature'),
            humidity=data.get('humidity'),
            motion=data.get('motion'),
            light=data.get('light')
        )
        db.session.add(new_data)
        db.session.commit()
        
        # --- AI Automation Logic Trigger ---
        ai_action_taken = False
        message = "Data saved successfully."
        
        if ML_AVAILABLE:
             # Run prediction using the new sensor data
             decision, confidence = predict_device_state(
                 temp=new_data.temperature,
                 humidity=new_data.humidity,
                 motion=new_data.motion,
                 light=new_data.light
             )
             
             # Apply decision to relevant device (e.g., Living Room Light)
             if decision is not None and confidence > 0.7:  # 70% confidence threshold
                 light_device = Device.query.filter_by(name="Living Room Light").first()
                 
                 expected_status = "ON" if decision == 1 else "OFF"
                 
                 if light_device and light_device.status != expected_status:
                     # State change needed
                     light_device.status = expected_status
                     
                     # Log the AI action
                     log = AutomationLog(
                         device_id=light_device.id,
                         action=f"Turned {expected_status}",
                         trigger_type="AI",
                         confidence_score=confidence
                     )
                     db.session.add(log)
                     db.session.commit()
                     ai_action_taken = True
                     message += f" AI triggered light {expected_status}."

        return jsonify({
            "message": message,
            "ai_action_taken": ai_action_taken,
            "data": new_data.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@api_blueprint.route('/sensors/history', methods=['GET'])
def get_sensor_history():
    limit = request.args.get('limit', 20, type=int)
    # Get latest data, order by desc, limit, then reverse to chronological
    data = SensorData.query.order_by(SensorData.timestamp.desc()).limit(limit).all()
    data.reverse()
    return jsonify([d.to_dict() for d in data])

@api_blueprint.route('/devices', methods=['GET'])
def get_devices():
    devices = Device.query.all()
    return jsonify([d.to_dict() for d in devices])

@api_blueprint.route('/devices/<int:device_id>/toggle', methods=['POST'])
def toggle_device(device_id):
    device = Device.query.get_or_404(device_id)
    
    # Toggle logic
    new_status = 'OFF' if device.status == 'ON' else 'ON'
    device.status = new_status
    
    # Log manual action
    log = AutomationLog(
        device_id=device.id,
        action=f"Turned {new_status}",
        trigger_type="Manual",
        confidence_score=1.0
    )
    
    db.session.add(log)
    db.session.commit()
    
    return jsonify({
        "message": f"Device {device.name} toggled to {new_status}",
        "device": device.to_dict()
    })

@api_blueprint.route('/logs', methods=['GET'])
def get_logs():
    limit = request.args.get('limit', 10, type=int)
    logs = AutomationLog.query.order_by(AutomationLog.timestamp.desc()).limit(limit).all()
    return jsonify([l.to_dict() for l in logs])

@api_blueprint.route('/status', methods=['GET'])
def system_status():
    return jsonify({
        "status": "online",
        "ai_enabled": ML_AVAILABLE
    })
