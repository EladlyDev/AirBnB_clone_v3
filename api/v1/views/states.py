#!/usr/bin/python3
"""
Defines routes to handle requests to state:
- get states
- get state with id
- create a new state
- delete a state
- update a state
"""
from api.v1.views import app_views
from models import storage
from models.state import State
from flask import jsonify, abort, request


@app_views.route('/states', methods=['GET', 'POST'], strict_slashes=False)
def states():
    """ Retrieves the list of all State objects """

    if request.method == 'GET':
        states = [state.to_dict() for state in storage.all(State).values()]
        return jsonify(states)

    if request.method == 'POST':
        if not request.get_json():
            abort(400, "Not a JSON")

        if 'name' not in request.get_json():
            abort(400, "Missing name")

        new_state = State(name=request.get_json()['name'])
        storage.new(new_state)
        storage.save()

        return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def state_get(id):
    """ GET, DELETE, PUT requests handler
    If the state_id is not linked to any State object, raise a 404 error
    """
    state = storage.get(State, id)
    if not state:
        abort(404)

    if request.method == 'GET':
        return state.to_dict()

    if request.method == 'DELETE':
        storage.delete(state)
        storage.save()
        del state
        return {}

    if request.method == 'PUT':
        data = request.get_json()

        if not data:
            abort(400, 'Not a JSON')

        for k, v in data.items():
            if k not in ['id', 'created_at', 'updated_at']:
                setattr(state, k, v)

        state.save()
        return jsonify(state.to_dict())
