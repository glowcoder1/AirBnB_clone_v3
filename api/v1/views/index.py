#!/usr/bin/python3
"""
index
"""


from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def get_status():
    return jsonify({'status': "OK"})

@app_views.route("/stats", methods=['GET'], strict_slashes=False)
def stats():
    """
    stats of all objs route
    returns json of all objs
    """
    data = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User"),
    }

    response = jsonify(data)
    response.status_code = 200

    return response
