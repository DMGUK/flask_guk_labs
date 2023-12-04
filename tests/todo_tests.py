import unittest

from flask import url_for

from app import db
from app.accounts.models import Users
from app.todo.models import Todo
from tests.base import BaseTestCase


class TodoTests(BaseTestCase):
    def test_todo_create(self):
        """
        Test creation of a todo item by making a POST request and verifying the created todo's title.
        """
        data = {
            'title': 'Write flask tests',
            'description': 'New description',
        }
        with self.client:
            response = self.client.post(url_for('todo.add_todo'), data=data,
                                        follow_redirects=True)
            assert response.status_code == 200
            todo = Todo.query.get(1)
            assert todo.title == data['title']

    def test_get_all_todo(self):
        """
        Test retrieving all todo items from the database and asserting the count to be 2.
        """
        todo_1 = Todo(title="todo1", description="description1", complete=False)
        todo_2 = Todo(title="todo2", description="description2", complete=False)
        db.session.add_all([todo_1, todo_2])
        all_todo = Todo.query.count()
        assert all_todo == 2

    def test_update_todo_complete(self):
        """
        Test updating a todo item to 'complete' status and verifying the change in status.
        """
        user = Users(username='test_user', email='test@example.com', password='password', image_file='image1.png')
        db.session.add(user)
        todo_1 = Todo(title="todo1", description="description1", complete=False)
        db.session.add(todo_1)
        db.session.commit()
        with self.client:
            response = self.client.post(
                url_for('accounts.login'),
                data=dict(email='test@example.com', password='password', remember=True),
                follow_redirects=True
            )
            assert response.status_code == 200
            response = self.client.get(url_for('todo.update_todo', todo_id=1),
                                       follow_redirects=True)
            todo = Todo.query.get(1)
            assert todo.complete is True

    def test_update_todo_incomplete(self):
        """
        Test updating a todo item to 'incomplete' status and verifying the change in status.
        """
        user = Users(username='test_user', email='test@example.com', password='password', image_file='image1.png')
        db.session.add(user)
        todo_1 = Todo(title="todo1", description="description1", complete=True)
        db.session.add(todo_1)
        db.session.commit()
        with self.client:
            response = self.client.post(
                url_for('accounts.login'),
                data=dict(email='test@example.com', password='password', remember=True),
                follow_redirects=True
            )
            assert response.status_code == 200
            response = self.client.get(url_for('todo.update_todo', todo_id=1),
                                       follow_redirects=True)
            todo = Todo.query.get(1)
            assert todo.complete is False

    def test_delete_todo(self):
        """
        Test deleting a todo item from the database and asserting its deletion.
        """
        user = Users(username='test_user', email='test@example.com', password='password', image_file='image1.png')
        db.session.add(user)
        todo = Todo(title="todo", description="description", complete=False)
        db.session.add(todo)
        db.session.commit()
        with self.client:
            response = self.client.post(
                url_for('accounts.login'),
                data=dict(email='test@example.com', password='password', remember=True),
                follow_redirects=True
            )
            assert response.status_code == 200
            response = self.client.post(url_for('todo.delete_todo', todo_id=1), follow_redirects=True)
            assert response.status_code == 200
            deleted_todo = Todo.query.get(1)
            assert deleted_todo is None

    def test_todo_page_view(self):
        """
        Test rendering the 'Todo list' page after logging in and checking for its successful loading.
        """
        user = Users(username='test_user', email='test@example.com', password='password', image_file='image1.png')
        db.session.add(user)
        db.session.commit()
        with self.client:
            response = self.client.post(
                url_for('accounts.login'),
                data=dict(email='test@example.com', password='password', remember=True),
                follow_redirects=True
            )
            response = self.client.get(url_for('todo.todo_list'), follow_redirects=True)
            assert response.status_code == 200
            self.assertIn(b'Todo list', response.data)


if __name__ == "__main__":
    unittest.main()