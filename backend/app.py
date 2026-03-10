from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_login import LoginManager
from config import Config
from models import db, Device, SensorData, AutomationLog, User
from routes.api import api_blueprint
from routes.views import views_blueprint
import threading

def create_app():
    app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/static')
    CORS(app)
    
    # Load configuration
    app.config.from_object(Config)
    
    # Initialize Database
    db.init_app(app)
    
    # Initialize Login Manager
    login_manager = LoginManager()
    login_manager.login_view = 'views.login'
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    # Register Blueprints
    app.register_blueprint(api_blueprint, url_prefix='/api')
    app.register_blueprint(views_blueprint)
    
    # Create tables if they don't exist
    with app.app_context():
        db.create_all()
        # Ensure dummy devices exist
        if not Device.query.first():
            dummy_devices = [
                Device(name="Living Room Light", type="Light"),
                Device(name="AC", type="Appliance"),
                Device(name="Main Door Lock", type="Security")
            ]
            db.session.add_all(dummy_devices)
            db.session.commit()
            
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
