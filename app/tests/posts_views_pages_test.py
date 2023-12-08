from flask import url_for
from app.tests.conftest import client, init_database, log_in_default_user


def test_all_posts_page_loads(client):
    response = client.get(url_for('posts.view_posts'))
    assert response.status_code == 200
    assert b'List of Posts' in response.data


def test_post_create_page_loads(client, init_database, log_in_default_user):
    response = client.get(url_for('posts.create_post'))
    assert response.status_code == 200
    assert b'Create New Post' in response.data


def test_post_by_id_page_loads(client, init_database):
    response = client.get(url_for('posts.view_post', id=1))
    assert response.status_code == 200
    assert b'Created at: ' in response.data


def test_post_edit_page_loads(client, init_database, log_in_default_user):
    response = client.get(url_for('posts.update_post', id=1))
    assert response.status_code == 200
    assert b'Post Update' in response.data