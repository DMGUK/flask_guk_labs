from flask import jsonify, request
from flask_httpauth import HTTPBasicAuth
from flask_jwt_extended import (jwt_required, create_access_token,
create_refresh_token, get_jwt_identity, get_jwt)
from . import api
from app.todo.models import Todo
from config import ACCESS_EXPIRES
from .. import db, bcrypt, jwt_manager, jwt_redis_blocklist
from ..accounts.models import Users

basic_auth = HTTPBasicAuth()


@basic_auth.verify_password
def verify_password(username, password):
    user = Users.query.filter_by(username=username).first()
    if user and bcrypt.check_password_hash(user.password, password):
        return username


@basic_auth.error_handler
def auth_error(status):
    return jsonify(message="You have inputted the wrong data for authorization"), status


@api.route('/login', methods=['POST'])
@basic_auth.login_required
def login():
    access_token = create_access_token(identity=basic_auth.current_user())
    refresh_token = create_refresh_token(identity=basic_auth.current_user())
    return jsonify(access_token=access_token, refresh_token=refresh_token)


@api.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify(msg="Token was refreshed successfully", access_token=access_token)


@jwt_manager.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
    jti = jwt_payload["jti"]
    token_in_redis = jwt_redis_blocklist.get(jti)
    return token_in_redis is not None


@api.route("/logout", methods=["DELETE"])
@jwt_required(verify_type=False)
def logout():
    token = get_jwt()
    jti = token["jti"]
    ttype = token["type"]
    jwt_redis_blocklist.set(jti, "", ex=ACCESS_EXPIRES[ttype])

    return jsonify(msg=f"{ttype.capitalize()} token successfully revoked")


@api.route('/todos', methods=['GET'])
def get_todos():
    todos = Todo.query.all()
    todo_dict = [
        {
            'id': t.id,
            'title': t.title,
            'description': t.description,
            'complete': t.complete
        }
        for t in todos
    ]
    return jsonify(todo_dict)

@api.route('/todos', methods=['POST'])
@jwt_required()
def new_todo():
    todo_new = request.get_json()
    title = todo_new.get('title')
    description = todo_new.get('description')

    if not (title and description):
        return jsonify('Invalid input data'), 400

    todo = Todo(title=title, description=description, complete=False)
    db.session.add(todo)
    db.session.commit()

    return jsonify({"id": todo.id, "title": todo.title}), 201

@api.route('/todos/<int:id>', methods=['GET'])
def get_todo(id):
    todo = Todo.query.get(id)

    if not todo:
        return jsonify(f'No todo with id {id}'), 404

    item = {
        "id": todo.id,
        "title": todo.title,
        "description": todo.description,
        "complete": todo.complete
    }

    return jsonify(item)

@api.route('/todos/<int:id>', methods=['PUT'])
@jwt_required()
def update_todo(id):
    todo = Todo.query.get(id)

    if not todo:
        return jsonify({"message": f"Todo with id = {id} not found"}), 404

    new_data = request.get_json()

    if not new_data:
        return jsonify({"message": "No input data provided"}), 400

    if 'title' in new_data:
        todo.title = new_data['title']

    if 'description' in new_data:
        todo.description = new_data['description']

    db.session.commit()

    return jsonify({"message": "Todo was updated"}), 200

@api.route('/todos/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_todo(id):
    todo = Todo.query.get(id)

    if not todo:
        return jsonify(f'No todo with id {id}'), 404

    db.session.delete(todo)
    db.session.commit()

    return jsonify({"message": "Todo was deleted"}), 200
