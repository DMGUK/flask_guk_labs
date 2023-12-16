import os
from datetime import timedelta

from dotenv import load_dotenv

load_dotenv('database_link.env')
app_root_path = os.path.dirname(os.path.abspath(__file__))

ACCESS_EXPIRES = {
    'access': timedelta(minutes=30),
    'refresh': timedelta(days=1)
}

class Config:
    SECRET_KEY = b"secretkey"
    WTF_CSRF_ENABLED = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = "super-secret"
    JWT_ACCESS_TOKEN_EXPIRES = ACCESS_EXPIRES['access']
    JWT_REFRESH_TOKEN_EXPIRES = ACCESS_EXPIRES['refresh']

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f'{os.getenv("DB_URL")}'

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = f'{os.getenv("DB_URL")}'

class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
