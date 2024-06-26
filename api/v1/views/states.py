#!/usr/bin/python3
"""
route for handling State interaction
"""
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.state import State


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def state_get_all():
    """
    retrieves State objects
    returns json of all states
    """
    states = []
    state_obj = storage.all("State")
    for obj in state_obj.values():
        states.append(obj.to_json())

    return jsonify(states)


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def state_create():
    """
    create state route
    returns created state obj
    """
    state_obj = request.get_json(silent=True)
    if state_obj is None:
        abort(400, 'Not a JSON')
    if "name" not in state_obj:
        abort(400, 'Missing name')

    new_state = State(**state_obj)
    new_state.save()
    response = jsonify(new_state.to_json())
    response.status_code = 201

    return response


@app_views.route("/states/<state_id>",  methods=["GET"], strict_slashes=False)
def state_by_id(state_id):
    """
    gets a  State object by ID
    returns state obj with the specified id or error
    """

    data = storage.get("State", str(state_id))

    if data is None:
        abort(404)

    return jsonify(data.to_json())


@app_views.route("/states/<state_id>",  methods=["PUT"], strict_slashes=False)
def state_put(state_id):
    """
    updates specific State object by ID
    returns state object and 200 on success, or 400 or 404 on failure
    """
    state_json = request.get_json(silent=True)
    if state_json is None:
        abort(400, 'Not a JSON')
    fetched_obj = storage.get("State", str(state_id))
    if fetched_obj is None:
        abort(404)
    for key, val in state_json.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(fetched_obj, key, val)
    fetched_obj.save()
    return jsonify(fetched_obj.to_json())


@app_views.route("/states/<state_id>", methods=["DELETE"],
                 strict_slashes=False)
def state_delete_by_id(state_id):
    """
    deletes State by id
    returns empty dict with 200 or 404 if not found
    """

    fetched_obj = storage.get("State", str(state_id))

    if fetched_obj is None:
        abort(404)

    storage.delete(fetched_obj)
    storage.save()

    return jsonify({})
