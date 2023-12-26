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
    OPENAPI_VERSION = "3.0.3"
    OPENAPI_URL_PREFIX = "/api_accounts"
    OPENAPI_SWAGGER_UI_PATH = "/swagger-ui"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f'{os.getenv("DB_URL")}'
    REDIS_DB_URI = 'redis://localhost:6379'

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DB_URL')
    REDIS_DB_URI = os.environ.get('REDIS_DB_URL')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    FLASK_SECRET = SECRET_KEY

class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
