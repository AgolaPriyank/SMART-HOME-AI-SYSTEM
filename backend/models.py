from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Device(db.Model):
    __tablename__ = 'devices'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(100))
    status = db.Column(db.String(10), default='OFF') # ON or OFF
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'status': self.status
        }

class SensorData(db.Model):
    __tablename__ = 'sensor_data'
    id = db.Column(db.Integer, primary_key=True)
    temperature = db.Column(db.Float)
    humidity = db.Column(db.Float)
    motion = db.Column(db.Boolean)
    light = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'temperature': self.temperature,
            'humidity': self.humidity,
            'motion': self.motion,
            'light': self.light,
            'timestamp': self.timestamp.isoformat()
        }

class AutomationLog(db.Model):
    __tablename__ = 'automation_logs'
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.Integer, db.ForeignKey('devices.id'))
    action = db.Column(db.String(50))
    trigger_type = db.Column(db.String(20), default='Manual') # Manual or AI
    confidence_score = db.Column(db.Float, default=0.0)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    device = db.relationship('Device', backref=db.backref('logs', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'device_name': self.device.name if self.device else "Unknown",
            'action': self.action,
            'trigger_type': self.trigger_type,
            'confidence_score': self.confidence_score,
            'timestamp': self.timestamp.isoformat()
        }
