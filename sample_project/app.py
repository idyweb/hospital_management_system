from flask import Flask
from flask_migrate import Migrate
from sample_project.extensions import db

from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
import os

from flask_restx.apidoc import apidoc

load_dotenv() 


ROOT_URL = '/sample_project'


def create_app(config_name):
    from sample_project.config import app_config

    app = Flask(__name__)
    app.config.from_object(app_config[config_name])
    app.config["APPLICATION_ROOT"] = ROOT_URL
    
    
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI")
    
    app.config['SECURITY_PASSWORD_SALT'] = os.getenv("SECURITY_PASSWORD_SALT")
    app.config['SECURITY_REGISTERABLE'] = os.getenv("SECURITY_REGISTERABLE")
    app.config['SECURITY_SEND_REGISTER_EMAIL'] = os.getenv("SECURITY_SEND_REGISTER_EMAIL")
    app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
    jwt = JWTManager(app)
    migrate = Migrate(app, db)
    


    with app.app_context():
        from sample_project.api_v1 import blueprint as api
        from sample_project.healthcheck import healthcheck

        app.register_blueprint(api, url_prefix=ROOT_URL + '/api/v1.0')
        app.register_blueprint(healthcheck, url_prefix=ROOT_URL + '/version')
        extensions(app)
        db.create_all()
    return app

def extensions(app):
    db.init_app(app)