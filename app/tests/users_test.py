from flask_login import current_user

from app import db
from app.accounts.models import Users
from app.tests.conftest import client, init_database, log_in_default_user
from flask import url_for


def test_user_model():
    user = Users("user", "user@gmail.com", "password", "image.png")
    assert user.username == 'user'
    assert user.email == 'user@gmail.com'
    assert user.image_file == 'image.png'
    assert user.password != 'password'


def test_register_user(client):
    response = client.post(
        url_for('accounts.signup'),
        data=dict(
            username='michael',
            email='michael@realpython.com',
            password='123456',
            confirm_password='123456'
        ),
        follow_redirects=True
    )
    assert response.status_code == 200
    assert b'You have successfully signed up' in response.data


def test_login_user(client, init_database):
    find_user = Users.query.filter_by(email='patkennedy24@gmail.com').first()
    response = client.post(
        url_for('accounts.login', external=True),
        data=dict(
            email='patkennedy24@gmail.com',
            password='FlaskIsAwesome',
            remember = True
        ),
        follow_redirects=True
    )
    assert response.status_code == 200
    assert current_user.is_authenticated == True
    assert b"You have logged in" in response.data


def test_login_user_with_fixture(client, init_database, log_in_default_user):
    assert current_user.is_authenticated == True
  

def test_log_out_user(client, log_in_default_user):
    response = client.get(
        url_for('accounts.logout'),
        follow_redirects=True
    )

    assert b'You have logged out', response.data
    assert response.status_code == 200
    assert current_user.is_authenticated == False