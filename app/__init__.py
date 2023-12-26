import os

from flask import Flask
from flask_bcrypt import Bcrypt
import redis
from flask_httpauth import HTTPBasicAuth
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

import config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
jwt_manager = JWTManager()
url = config.ProductionConfig.REDIS_DB_URI
jwt_redis_blocklist = redis.from_url(url)
def create_app(config_name='development'):
    app = Flask(__name__)

    from config import DevelopmentConfig, ProductionConfig, TestingConfig

    if config_name == 'production':
        app.config.from_object(ProductionConfig)
    elif config_name == 'testing':
        app.config.from_object(TestingConfig)
    else:
        app.config.from_object(DevelopmentConfig)

    db.init_app(app)
    Migrate(app, db)
    bcrypt.init_app(app)
    jwt_manager.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'accounts.login'
    login_manager.login_message_category = 'info'


    with app.app_context():
        from .portfolio.views import portfolio
        from .cookies.views import cookies
        from .accounts.views import accounts
        from .todo.views import todo
        from .feedback.views import feedback
        from .posts.views import posts
        from .api.views import api
        from .api_accounts.views import api_accounts
        from .swagger import swaggerui_blueprint

        app.register_blueprint(accounts)
        app.register_blueprint(portfolio)
        app.register_blueprint(cookies)
        app.register_blueprint(todo)
        app.register_blueprint(feedback)
        app.register_blueprint(posts)
        app.register_blueprint(api)
        app.register_blueprint(api_accounts)
        app.register_blueprint(swaggerui_blueprint, url_prefix='/swagger')

    return app
