#!/usr/bin/python3
""" the view for the amenities """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.amenity import Amenity
from os import environ
storage_t = environ.get('HBNB_TYPE_STORAGE')


@app_views.route('/places/<place_id>/amenities', strict_slashes=False)
def place_amenities_route(place_id):
    """ Retrieves the list of all Amenity objects of a Place """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    amenities = []
    if storage_t != 'db':
        amenities = place.amenity_ids
    else:
        amenities = place.amenities
    amenities = [amenity.to_dict() for amenity in amenities]
    return jsonify(amenities)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE', 'POST'],
                 strict_slashes=False)
def place_amenity_route(place_id, amenity_id):
    """ the Delete and Post http requests """
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if not place or not amenity:
        abort(404)

    if request.method == 'DELETE':
        place_amenities = []
        if storage_t == 'db':
            place_amenities = place.amenities
        else:
            place_amenities = place.amenity_ids
        if amenity not in place_amenities:
            abort(404)
        place_amenities.remove(amenity)
        place.save()
        return {}
    elif request.method == 'POST':
        place_amenities = []
        if storage_t == 'db':
            place_amenities = place.amenities
        else:
            place_amenities = place.amenity_ids
        if amenity in place_amenities:
            return amenity.to_dict()
        place_amenities.append(amenity)
        place.save()

        return amenity.to_dict(), 201
