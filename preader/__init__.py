from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    '''Create an instance off app with config below'''
    # App Config
    app = Flask(__name__)
    # Secret key provided for local test running, changed for production
    app.config['SECRET_KEY'] = '4af2a2635a94e6e39a49e2e8d3c3f9e33d03823fed66bde2'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///preader.db'
    db.init_app(app)
    # Blueprints
    from .routes import main
    from .errors import error

    app.register_blueprint(main)
    app.register_blueprint(error)

    return app
