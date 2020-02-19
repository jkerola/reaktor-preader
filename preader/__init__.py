from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config

db = SQLAlchemy()
app = Flask(__name__)


def create_app(config=Config):
    '''Create an instance off app with config below'''
    # App Config
    app.config.from_object(config)
    db.init_app(app)
    
    # Blueprints
    from .routes import main
    from .errors import error

    app.register_blueprint(main)
    app.register_blueprint(error)

    return app
