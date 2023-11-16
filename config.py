import os
from dotenv import load_dotenv
load_dotenv('database_link.env')


UPLOAD_FOLDER = 'app/static/profile_images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'jfif', 'webp'}
MAX_IMAGE_SIZE = (200, 200)
SECRET_KEY = b"secretkey"
WTF_CSRF_ENABLED = True
SQLALCHEMY_DATABASE_URI = f'{os.getenv("DB_URL")}'
SQLALCHEMY_TRACK_MODIFICATIONS = False
