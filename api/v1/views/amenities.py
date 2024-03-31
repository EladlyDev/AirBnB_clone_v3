#!/usr/bin/python3
"""
Defines routes to handle requests to amenity:
- get amenities
- get amenity with id
- create a new amenity
- delete a amenity
- update a amenity
"""
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from flask import jsonify, abort, request, make_response


@app_views.route('/amenities', methods=['GET', 'POST'], strict_slashes=False)
def amenities():
    """ Retrieves the list of all Amenity objects """

    if request.method == 'GET':
        amenities = [amenity.to_dict() for amenity
                     in storage.all(Amenity).values()]
        return jsonify(amenities)

    if request.method == 'POST':
        if request.content_type != "application/json":
            abort(400, description="Not a JSON")

        if not request.get_json():
            abort(400, description="Not a JSON")

        if 'name' not in request.get_json():
            abort(400, description="Missing name")

        new_amenity = Amenity(name=request.get_json()['name'])
        storage.new(new_amenity)
        storage.save()

        return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<string:id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def amenity(id):
    """ GET, DELETE, PUT requests handler
    If the amenity_id is not linked to any Amenity object, raise a 404 error
    """
    amenity = storage.get(Amenity, id)
    if not amenity:
        abort(404)

    if request.method == 'GET':
        return amenity.to_dict()

    if request.method == 'DELETE':
        storage.delete(amenity)
        storage.save()
        del amenity
        return {}

    if request.method == 'PUT':
        if request.content_type != "application/json":
            abort(400, description="Not a JSON")

        data = request.get_json()
        if not data:
            abort(400, description='Not a JSON')

        amenity.name = data.get('name', amenity.name)

        amenity.save()
        return jsonify(amenity.to_dict())
