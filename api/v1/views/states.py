#!/usr/bin/python3
"""
Defines routes to handle requests to state:
- get states
- get state with id
- create a new state
- delete a state
- update a state
"""

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    return jsonify(list(
        x.to_dict() for x in list(storage.all(State).values())
        ))


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    state_of_id = storage.get(State, state_id)
    if state_of_id:
        return (jsonify(state_of_id.to_dict()))
    abort(404)


@app_views.route('/states/<state_id>',
                 methods=['DELETE'],
                 strict_slashes=False
                 )
def delete_state(state_id):
    state_of_id = storage.get(State, state_id)
    if state_of_id:
        storage.delete(state_of_id)
        storage.save()
        return (jsonify({}))
    abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    if not request.get_json():
        abort(400, "Not a JSON")
    if 'name' not in request.get_json():
        abort(400, "Missing name")
    new_state = State(name=request.get_json()['name'])
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    for k, v in request.get_json().items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(state, k, v)
    state.save()
    return jsonify(state.to_dict())
