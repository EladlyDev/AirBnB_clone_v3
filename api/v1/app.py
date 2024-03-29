#!/usr/bin/python3
"""
create an app instanse and register it to app_views
customize 404 error
"""

from flask import Flask, make_response
from models import storage
from api.v1.views import app_views
from os import environ


app = Flask(__name__)
app.register_blueprint(app_views)


@app.errorhandler(404)
def not_found(err):
    return make_response({'error': 'Not found'}, 404)


@app.teardown_appcontext
def teardown(exception):
    """ gets called after each request """
    storage.close()


if __name__ == '__main__':
    host = environ.get('HBNB_API_HOST', '0.0.0.0')
    port = environ.get('HBNB_API_PORT', '5000')
    app.run(host=host, port=port, threaded=True, debug=True)
