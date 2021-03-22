import os


basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'ba6937627292998bea63445ef3423fedd1987d84595131'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    
    SERVER_NAME = os.environ.get('SERVER_NAME') or None
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ENC_KEY = os.environ.get('ENC_KEY') or "ba6937627292998b"
    
