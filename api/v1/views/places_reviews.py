#!/usr/bin/python3
""" the view for the reviews """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods={'GET', 'POST'},
                 strict_slashes=False)
def reviews(place_id):
    """ Retrieves the list of all Review objects of a Place """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    if request.method == 'GET':
        reviews = [review.to_dict() for review in place.reviews]
        return jsonify(reviews)
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

        data['place_id'] = place_id
        new_review = Review(**data)
        new_review.save()
        return new_review.to_dict(), 201


@app_views.route('/reviews/<review_id>', methods={'GET', 'DELETE', 'PUT'},
                 strict_slashes=False)
def review(review_id):
    """ all handlers for http of review requests """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    if request.method == 'GET':
        return review.to_dict()
    elif request.method == 'DELETE':
        storage.delete(review)
        storage.save()
        return {}
    elif request.method == 'PUT':
        data = request.get_json()
        if not data:            # ############# checker error might be here
            abort(400, 'Not a JSON')

        for k, v in data.items():
            if k not in ['id', 'user_id', 'place_id', 'created_at',
                         'updated_at']:
                setattr(review, k, v)
        review.save()
        return review.to_dict()
