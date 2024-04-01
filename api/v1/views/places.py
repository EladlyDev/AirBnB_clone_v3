#!/usr/bin/python3
""" the view for the places """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
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
    """ Retrieves the list of all Places filtered by state,
    city and amenities """

    # 1. if not valid json abort 400 'Not a JSON'
    if request.content_type != "application/json":
        abort(400, description="Not a JSON")

    places = storage.all(Place).values()

    # 2. if json body is empty or all keys are empty
    data = request.get_json()
    states_ids = data.get('states', [])
    cities_ids = data.get('cities', [])
    amenities_ids = data.get('amenities', [])
    if not data or not (states_ids or cities_ids or amenities_ids):
        return jsonify([place.to_dict() for place in places])

    # 3. if states or cities not empty, retreive them all
    states = [storage.get(State, id) for id in states_ids]
    cities = [storage.get(City, id) for id in cities_ids]

    # drop none values in states and cities lists that comes if storage.get returns None
    states = [state for state in states if state]
    cities = [city for city in cities if city]

    # 4. retrieve all places in the states and its cities
    # plus all in the cities unless if it is already listed by the states
    states_cities = [city for state in states for city in state.cities]
    req_cities = [city for city in cities if city not in states_cities]
    req_cities.extend(states_cities)

    # 5. if amenities is not empty, than return all places
    # with the specified  amenities only, no more, no less.
    amenities = [storage.get(Amenity, id) for id in amenities_ids]
    req_places = [place for city in req_cities
                  for place in city.places]

    if not req_places:
        req_places = storage.all(Place).values()

    req_places = [place.to_dict() for place in req_places if
                  all(amenity in place.amenities
                      for amenity in amenities)]

    return jsonify(req_places)
