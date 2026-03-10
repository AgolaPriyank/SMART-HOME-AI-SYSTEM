import os

class Config:
    # Use SQLite for easy setup as requested in the plan
    # In a real production scenario, this would be a MySQL URI
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///../database/smarthome.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a-very-secret-smart-home-key'
