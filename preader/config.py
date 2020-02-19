import os


class Config(object):
    '''Configuration class for application creation'''
    # Secret key provided for local test running, changed for production
    SECRET_KEY = os.environ.get('SECRET_KEY') or '4af2a2635a94e6e39a49e2e8d3c3f9e33d03823fed66bde2'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///preader.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = './static/uploads'
