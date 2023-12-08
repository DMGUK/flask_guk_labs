from flask import url_for
from app.tests.conftest import client, init_database, log_in_default_user

def test_all_todo_page_loads(client, init_database, log_in_default_user):
    response = client.get(url_for('todo.todo_list'))
    assert response.status_code == 200
    assert b'Todo list' in response.data


def test_all_feedback_page_loads(client, init_database, log_in_default_user):
    response = client.get(url_for('feedback.feedback_list'))
    assert response.status_code == 200
    assert b'Feedbacks' in response.data

