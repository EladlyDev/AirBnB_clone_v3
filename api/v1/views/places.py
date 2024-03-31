#!/usr/bin/python3
""" the view for the places """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<city_id>/places', methods={'GET', 'POST'},
                 strict_slashes=False)
def places(city_id):
    """ Retrieves the list of all Place objects of a City """
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    if request.method == 'GET':
        places = [place.to_dict() for place in city.places]
        return jsonify(places)
    elif request.method == 'POST':
        data = request.get_json()
        if not data:            # ############# checker error might be here
            abort(400, 'Not a JSON')
        if 'user_id' not in data:
            abort(400, 'Missing user_id')
        if 'name' not in data:
            abort(400, 'Missing name')
        if not storage.get(User, data['user_id']):
            abort(404)

        data['city_id'] = city_id
        new_place = Place(**data)
        new_place.save()
        return new_place.to_dict(), 201


@app_views.route('/places/<place_id>', methods={'GET', 'DELETE', 'PUT'},
                 strict_slashes=False)
def place(place_id):
    """ all handlers for http of place requests """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    if request.method == 'GET':
        return place.to_dict()
    elif request.method == 'DELETE':
        storage.delete(place)
        storage.save()
        return {}
    elif request.method == 'PUT':
        data = request.get_json()
        if not data:            # ############# checker error might be here
            abort(400, 'Not a JSON')

        for k, v in data.items():
            if k not in ['id', 'user_id', 'city_id', 'created_at',
                         'updated_at']:
                setattr(place, k, v)
        place.save()
        return place.to_dict()
