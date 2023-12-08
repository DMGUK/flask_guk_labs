from flask import url_for
from app.tests.conftest import client, init_database, log_in_default_user

def test_signup_page_loads(client):
    response = client.get(url_for('accounts.signup'))
    assert response.status_code == 200
    assert b'Sign Up form' in response.data


def test_login_page_loads(client):
    response = client.get(url_for('accounts.login'))
    assert response.status_code == 200
    assert b'Login form' in response.data


def test_post_account_page_loads(client, init_database, log_in_default_user):
    response = client.get(url_for('accounts.account'))
    assert response.status_code == 200
    assert b'Your unique ID is' in response.data


def test_post_all_users_loads(client, init_database, log_in_default_user):
    response = client.get(url_for('accounts.users', id=1))
    assert response.status_code == 200
    assert b'List of users' in response.data


def test_post_edit_page_loads(client, init_database, log_in_default_user):
    response = client.get(url_for('accounts.change_password', id=1))
    assert response.status_code == 200
    assert b'Change your password' in response.data