#!/user/bin/python3
""" the view for the cities """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods={'GET', 'POST'},
                 strict_slashes=False)
def cities(state_id):
    """ Retrieves the list of all City objects of a State """
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    if request.method == 'GET':
        cities = [city.to_dict() for city in state.cities]
        return jsonify(cities)
    elif request.method == 'POST':
        data = request.get_json()
        if not data:            # ############# checker error might be here
            abort(400, 'Not a JSON')
        if 'name' not in data:
            abort(400, 'Missing name')
        data['state_id'] = state_id
        new_city = City(**data)
        new_city.save()
        return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods={'GET', 'DELETE', 'PUT'},
                 strict_slashes=False)
def city(city_id):
    """ all handlers for http of city requests """
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    if request.method == 'GET':
        return jsonify(city.to_dict())
    elif request.method == 'DELETE':
        storage.delete(city)
        storage.save()
        return {}
    elif request.method == 'PUT':
        data = request.get_json()
        if not data:            # ############# checker error might be here
            abort(400, 'Not a JSON')

        for k, v in data.items():
            if k not in ['id', 'state_id', 'created_at', 'updated_at']:
                setattr(city, k, v)
        city.save()
        return jsonify(city.to_dict())
