#!/usr/bin/python3
""" the view for the places """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
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
        if request.content_type != "application/json":
            abort(400, description="Not a JSON")

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
        if request.content_type != "application/json":
            abort(400, description="Not a JSON")

        data = request.get_json()
        if not data:
            abort(400, 'Not a JSON')

        for k, v in data.items():
            if k not in ['id', 'user_id', 'city_id', 'created_at',
                         'updated_at']:
                setattr(place, k, v)
        place.save()
        return place.to_dict()

@app_views.route('/places_search', methods=["POST"],
                 strict_slashes=False)
def places_search():
    """ Retrieves the list of all Places filtered by state, city and amenities """

    if request.content_type != "application/json":
        abort(400, description="Not a JSON")

    data = request.get_json()

    if ("states" not in data or not data["states"]) \
        and ("cities" not in data or not data["cities"]) \
        and ("amenities" not in data or not data["amenities"]):
        return jsonify([place.to_dict()
                        for place in storage.all(Place).values()
                        ])

    my_places_id = []
    my_cities_id = []
    
    if data["states"]:
        for state_id in data["states"]:
            my_cities_id.append(
                [x.id for x in storage.get(State, state_id).cities
                 ])

    if data["cities"]:
        for city_id in data["cities"]:
            my_cities_id.append(city_id)

    for city_id in my_cities_id:
        my_places_id.append([
            x.id for x in storage.get(City, city_id).places
            ])

    my_places_id = list(set(my_places_id))
    my_places = [storage.get(Place, x) for x in my_places_id]
    return jsonify([place.to_dict() for place in my_places])
