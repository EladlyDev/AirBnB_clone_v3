#!/usr/bin/python3
"""
Defines routes to handle requests to user:
- get users
- get user with id
- create a new user
- delete a user
- update a user
"""
from api.v1.views import app_views
from models import storage
from models.user import User
from flask import jsonify, abort, request, make_response


@app_views.route('/users', methods=['GET', 'POST'], strict_slashes=False)
def users():
    """ Retrieves the list of all User objects """

    if request.method == 'GET':
        users = [user.to_dict() for user
                 in storage.all(User).values()]
        return jsonify(users)

    if request.method == 'POST':
        if request.content_type != "application/json":
            abort(400, description="Not a JSON")

        if not request.get_json():
            abort(400, description="Not a JSON")

        if 'name' not in request.get_json():
            abort(400, description="Missing name")

        new_user = User(name=request.get_json()['name'])
        storage.new(new_user)
        storage.save()

        return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<string:id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def user(id):
    """ GET, DELETE, PUT requests handler
    If the user_id is not linked to any User object, raise a 404 error
    """
    user = storage.get(User, id)
    if not user:
        abort(404)

    if request.method == 'GET':
        return user.to_dict()

    if request.method == 'DELETE':
        storage.delete(user)
        storage.save()
        del user
        return {}

    if request.method == 'PUT':
        if request.content_type != "application/json":
            abort(400, description="Not a JSON")

        data = request.get_json()

        if not data:
            abort(400, description='Not a JSON')

        user.name = data.get('name', user.name)

        user.save()
        return jsonify(user.to_dict())
