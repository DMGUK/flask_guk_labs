import os
from dotenv import load_dotenv
load_dotenv('migrations/database_link.env')


SECRET_KEY = b"secretkey"
WTF_CSRF_ENABLED = True
SQLALCHEMY_DATABASE_URI = f'{os.getenv("DB_URL")}'
SQLALCHEMY_TRACK_MODIFICATIONS = False
