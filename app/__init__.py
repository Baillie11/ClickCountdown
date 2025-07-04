from flask import Flask
from flask_login import LoginManager
from flask_pymongo import PyMongo
from config import Config

mongo = PyMongo()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def get_version():
    try:
        with open('VERSION') as f:
            return f.read().strip()
    except Exception:
        return 'unknown'

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    mongo.init_app(app)
    login_manager.init_app(app)

    from .auth import auth as auth_blueprint
    from .main import main as main_blueprint

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint)

    #print("Mongo DB object:", mongo.db)

    @app.context_processor
    def inject_version():
        return dict(app_version=get_version())

    return app
