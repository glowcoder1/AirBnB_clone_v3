#!/usr/bin/python3
"""
route for handling Amenity operations
"""
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def amenity_get_all():
    """
    retrieves all Amenity objects
    returns json of all states
    """
    amenities = []
    am_obj = storage.all("Amenity")
    for obj in am_obj.values():
        amenities.append(obj.to_json())

    return jsonify(amenities)


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def amenity_create():
    """
    create amenity route
    returns the created amenity obj
    """
    am_json = request.get_json(silent=True)
    if am_json is None:
        abort(400, 'Not a JSON')
    if "name" not in am_json:
        abort(400, 'Missing name')

    new_am = Amenity(**am_json)
    new_am.save()
    response = jsonify(new_am.to_json())
    response.status_code = 201

    return response


@app_views.route("/amenities/<amenity_id>",  methods=["GET"],
                 strict_slashes=False)
def amenity_by_id(amenity_id):
    """
    it gets a specific Amenity object by ID
    it returns state obj with the specified id or error
    """

    fetched_data = storage.get("Amenity", str(amenity_id))

    if fetched_data is None:
        abort(404)

    return jsonify(fetched_data.to_json())


@app_views.route("/amenities/<amenity_id>",  methods=["PUT"],
                 strict_slashes=False)
def amenity_put(amenity_id):
    """
    it updates specific Amenity object by ID
    param amenity_id: amenity object ID
    returns the amenity object and 200 on success, or 400 or 404 on failure
    """
    am_json = request.get_json(silent=True)
    if am_json is None:
        abort(400, 'Not a JSON')
    fetched_data = storage.get("Amenity", str(amenity_id))
    if fetched_data is None:
        abort(404)
    for key, val in am_json.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(fetched_data, key, val)
    fetched_data.save()
    return jsonify(fetched_data.to_json())


@app_views.route("/amenities/<amenity_id>",  methods=["DELETE"],
                 strict_slashes=False)
def amenity_delete_by_id(amenity_id):
    """
    deletes Amenity by id
    param amenity_id: Amenity object id
    return: empty obj  with 200 or 404 if not found
    """

    fetched_data = storage.get("Amenity", str(amenity_id))

    if fetched_data is None:
        abort(404)

    storage.delete(fetched_data)
    storage.save()

    return jsonify({})
