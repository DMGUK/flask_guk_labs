import unittest
from flask_testing import TestCase
from app import create_app, db, bcrypt
from app.accounts.models import Users


class BaseTestCase(TestCase):
    def create_app(self):
        app = create_app('testing')
        return app


    def setUp(self):
        db.create_all()
        user = Users(username='dmytro', email='dmytro@gmail.com',
                     password='dmytro_password_111', image_file='image_dmytro.png')
        db.session.add(user)
        db.session.commit()


    def tearDown(self):
        db.session.remove()
        db.drop_all()