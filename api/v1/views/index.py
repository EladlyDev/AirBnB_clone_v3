#!/usr/bin/python3
"""
Defines a route to show the status of the web app
Defines a route to show the states of the db
"""
from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status', strict_slashes=False)
def status():
    """ returns the status of the service """
    return {'status': 'OK'}


@app_views.route('/stats', strict_slashes=False)
def stats():
    from models.amenity import Amenity
    from models.city import City
    from models.place import Place
    from models.review import Review
    from models.state import State
    from models.user import User
    classes = {
        "amenities": Amenity,
        "cities": City,
        "places": Place,
        "reviews": Review,
        "states": State,
        "users": User
        }
    stats_dict = {key: storage.count(value)
                  for key, value in classes.items()
                  if storage.count(value) != 0
                  }
    return jsonify(stats_dict)
