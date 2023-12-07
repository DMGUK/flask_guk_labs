from flask import jsonify, request
from psycopg2 import IntegrityError

from . import api
from app.todo.models import Todo
from .. import db


@api.route('/ping', methods=['GET'])
def ping():
    return jsonify({"message" : "pong"})


@api.route('/todos', methods=['GET'])
def get_todos():
    todos = Todo.query.all()
    todo_dict = []
    for t in todos :
        item = dict(
            id = t.id,
            title = t.title,
            description = t.description,
            complete = t.complete
        )
        todo_dict.append(item)

    return jsonify(todo_dict)


@api.route('/todos', methods=['POST'])
def new_todo():
    new_todo = request.get_json()
    todo = Todo(title=new_todo.get('title'), description=new_todo.get('description'))
    todo.complete = False

    if not new_todo:
        return jsonify('no input data'), 400

    if not (new_todo.get('title') or new_todo.get('description')):
        return jsonify('no keys provided'), 422

    db.session.add(todo)
    db.session.commit()

    new_todo = Todo.query.filter_by(id=todo.id).first()

    return jsonify({"id":new_todo.id, "title":new_todo.title}), 201

@api.route('/todos/<int:id>', methods=['GET'])
def get_todo(id):
    todos = Todo.query.filter_by(id=id).first()

    if not todos:
        return jsonify(f'no todo with id {id}'), 404

    item = {
        "id":todos.id,
        "title":todos.title,
        "description":todos.description,
        "complete":todos.complete
    }

    return jsonify(item)


@api.route('/todos/<int:id>', methods=['PUT'])
def update_todo(id):
    todo = Todo.query.filter_by(id=id).first()

    if not todo:
        return jsonify({"message": f"todo with id = {id} not found"}), 404

    new_data = request.get_json()

    if not new_data:
        return jsonify({"message": "no input data provided"}), 400

    if new_data.get('title'):
        todo.title = new_data.get('title')

    if new_data.get('description'):
        todo.description = new_data.get('description')

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()

    return jsonify({
        "message": "todo was updated"
    }), 200


@api.route('/todos/<int:id>', methods=['DELETE'])
def delete_todo(id):
    todo = Todo.query.filter_by(id=id).first()

    if not todo:
        return jsonify(f'no todo with id {id}'), 404

    db.session.delete(todo)
    db.session.commit()

    return jsonify({
        "message": "todo was deleted"
    }), 200


