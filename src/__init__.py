from flask import Flask
from src.flask_serwer import mood_detector_blueprint

def create_app():
    app = Flask(__name__)
    app.register_blueprint(mood_detector_blueprint)
    return app