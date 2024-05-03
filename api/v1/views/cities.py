#!/usr/bin/python3
"""
route for handling Cities objects and operations
"""
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.city import City


@app_views.route("/states/<state_id>/cities", methods=["GET"],
                 strict_slashes=False)
def city_by_state(state_id):
    """
    retrieves all City objects from a specific state
    param: state_id
    returns json of all cities in a state or 404 on error
    """
    cities = []
    state_obj = storage.get("State", state_id)

    if state_obj is None:
        abort(404)
    for obj in state_obj.cities:
        cities.append(obj.to_json())

    return jsonify(cities)


@app_views.route("/states/<state_id>/cities", methods=["POST"],
                 strict_slashes=False)
def city_create(state_id):
    """
    creates city route
    param: state_id - state id
    returns the created city obj
    """
    city_json = request.get_json(silent=True)
    if city_json is None:
        abort(400, 'Not a JSON')

    if not storage.get("State", str(state_id)):
        abort(404)

    if "name" not in city_json:
        abort(400, 'Missing name')

    city_json["state_id"] = state_id

    new_city = City(**city_json)
    new_city.save()
    response = jsonify(new_city.to_json())
    response.status_code = 201

    return response


@app_views.route("/cities/<city_id>",  methods=["GET"],
                 strict_slashes=False)
def city_by_id(city_id):
    """
    gets a specific City object by ID
    param city_id: city object id
    returns city obj with the specified id or error
    """

    fetched_data = storage.get("City", str(city_id))

    if fetched_data is None:
        abort(404)

    return jsonify(fetched_data.to_json())


@app_views.route("cities/<city_id>",  methods=["PUT"], strict_slashes=False)
def city_put(city_id):
    """
    updates specific City object by ID
    param city_id: city object ID
    returns city object of id and 200 on success, or 400 or 404 on failure
    """
    city_json = request.get_json(silent=True)
    if city_json is None:
        abort(400, 'Not a JSON')
    fetched_data = storage.get("City", str(city_id))
    if fetched_data is None:
        abort(404)
    for key, val in city_json.items():
        if key not in ["id", "created_at", "updated_at", "state_id"]:
            setattr(fetched_data, key, val)
    fetched_data.save()
    return jsonify(fetched_data.to_json())


@app_views.route("/cities/<city_id>",  methods=["DELETE"],
                 strict_slashes=False)
def city_delete_by_id(city_id):
    """
    deletes City by idd
    returns an empty dict with 200 or 404 if not found
    """

    fetched_data = storage.get("City", str(city_id))

    if fetched_data is None:
        abort(404)

    storage.delete(fetched_data)
    storage.save()

    return jsonify({})
