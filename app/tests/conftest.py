import pytest
from flask import url_for

from app import create_app, db
from app.accounts.models import Users
from app.posts.models import Posts, Categories, Tags
from app.todo.models import Todo


@pytest.fixture(scope='module')
def client():
    app = create_app('testing')
    app.config['SERVER_NAME'] = '127.0.0.1:5000'

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()

@pytest.fixture()
def user_test():
    user = Users(username='brand_new', email='brand_new@example.com', password='password')
    return user

@pytest.fixture(scope='module')
def category():
    category = Categories(name="Category")
    yield category

@pytest.fixture(scope='module')
def todo():
    todo_1 = Todo(title="Todo 1", description="Todo description 1", complete=False)
    todo_2 = Todo(title="Todo 2", description="Todo description 2", complete=False)

    todo_list = [todo_1, todo_2]

    yield todo_list

@pytest.fixture(scope='module')
def tags():
    tag_1 = Tags(name="Tag 1")
    tag_2 = Tags(name="Tag 2")

    tags = [tag_1, tag_2]

    yield tags

@pytest.fixture(scope='module')
def posts(category, tags):
    post_1 = Posts(title="Um consequatur volupta", text='Qui deleniti voluptas', user_id=1, category=category, tags=tags)
    post_2 = Posts(title="Optio eum rerum", text='Cumque qui omnis voluptatem.', user_id=1, category=category, tags=tags)

    posts = [post_1, post_2]
    yield posts


@pytest.fixture(scope='module')
def init_database(client, category, posts, todo):
    # Insert user data
    default_user = Users(username='patkennedy', email='patkennedy24@gmail.com', image_file='image.png', password='FlaskIsAwesome')
    db.session.add(default_user)
    db.session.add(category)
    db.session.add(posts[0])
    db.session.add(posts[1])
    db.session.add(todo[0])
    db.session.add(todo[1])

    # Commit the changes for the users
    db.session.commit()

    yield  # this is where the testing happens!

@pytest.fixture(scope='function')
def log_in_default_user(client):
    client.post(url_for('accounts.login'),
                     data={'email': 'patkennedy24@gmail.com', 'password': 'FlaskIsAwesome', 'remember': True},
                     follow_redirects=True
                     )

    yield  # this is where the testing happens!

    client.get(url_for('accounts.logout'))