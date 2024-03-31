#!/usr/bin/python3
"""
create an app instanse and register it to app_views
customize 404 error
"""

from flask import Flask, make_response, jsonify
from models import storage
from api.v1.views import app_views
from os import environ


app = Flask(__name__)
app.register_blueprint(app_views)


@app.errorhandler(404)
def not_found(err):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def not_json_and_missing_name(err):
    return jsonify(error=str(err.description)), 400


@app.teardown_appcontext
def teardown(exception):
    """ gets called after each request """
    storage.close()


if __name__ == '__main__':
    host = environ.get('HBNB_API_HOST', '0.0.0.0')
    port = environ.get('HBNB_API_PORT', '5000')
    app.run(host=host, port=port, threaded=True)
