from flask import url_for


def test_homepage_loads(client):
    response = client.get(url_for('portfolio.homepage'))
    assert response.status_code == 200
    assert b'Homepage' in response.data


def test_about_me_loads(client, init_database, log_in_default_user):
    response = client.get(url_for('portfolio.about_me'))
    assert response.status_code == 200
    assert b'About Me' in response.data


def test_my_project_loads(client, init_database):
    response = client.get(url_for('portfolio.my_projects'))
    assert response.status_code == 200
    assert b'My Projects' in response.data


def test_my_experience_loads(client, init_database, log_in_default_user):
    response = client.get(url_for('portfolio.my_experience'))
    assert response.status_code == 200
    assert b'My Experience' in response.data


def test_contacts_loads(client, init_database, log_in_default_user):
    response = client.get(url_for('portfolio.contacts'))
    assert response.status_code == 200
    assert b'Contacts' in response.data