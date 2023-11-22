import os
import re
from decouple import config
from datetime import timedelta

BASE_DIR=os.path.dirname(os.path.realpath(__file__))

class Config:
    SECRET_KEY=config('SECRET_KEY', 'secret')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(minutes=30)
    JWT_SECRET_KEY=config('JWT_SECRET_KEY', 'jwt_secret_key')
    

class DevConfig(Config):
    DEBUG=True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO=True
    temp_uri = 'sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')
    SQLALCHEMY_DATABASE_URI= re.sub(r'\\', r'\\\\', temp_uri)

class TestConfig(Config):
    os.environ['FLASK_ENV'] = 'test'
    DEBUG=True
    TESTING = True
    SECRET_KEY=config('TEST_SECRET_KEY', 'secret')
    

class ProdConfig(Config):
    os.environ['FLASK_ENV'] = 'production'
    DEBUG=False
    ENV='production'

config_dict = {
    'dev': DevConfig,
    'test': TestConfig,
    'prod': ProdConfig
}