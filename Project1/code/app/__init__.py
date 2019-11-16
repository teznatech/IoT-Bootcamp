from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from app.controllers.cam.camera_pi import Camera
from app.controllers.cam.pantilt import PanTilt
from app.controllers.lights.light_control import LightControl
import os

db = SQLAlchemy()
camera = Camera()
pantilt = PanTilt()
lightControl = LightControl()

from app.controllers.routines.routine_control import RoutineControl
routineControl = RoutineControl()

basedir = os.path.abspath(os.path.dirname(__file__))

def create_app(config_class=Config):
    app = Flask(__name__, static_url_path='')
    app.config.from_object(config_class)
    db.init_app(app)
    with app.app_context():
        if not os.path.isfile('../app.db'):
            db.create_all()

    from app.main import bp as main_bp
    app.register_blueprint(main_bp, url_prefix='/main')

    from app.camera import bp as cam_bp
    app.register_blueprint(cam_bp, url_prefix='/cam')

    from app.light_controller import bp as light_bp
    app.register_blueprint(light_bp, url_prefix='/light')

    from app.routine_control import bp as routine_bp
    app.register_blueprint(routine_bp, url_prefix='/routine')

    from app.sensor import Sensor
    sensor = Sensor(app) #starts sensor lecture also
    sensor.read_data()

    return app

os.system('$(which python3) '+ os.path.join(basedir, 'controllers', 'lights', 'effects.py') +' 0.6')
os.system('$(which python3) '+ os.path.join(basedir, 'controllers', 'lights', 'lightController.py') +' 0 0 0 0')

from app import models
