#!/usr/bin/env python3

from flask import Flask, jsonify, abort, request, make_response, url_for
from jsonschema import validate

import idb
from idb.db import session_scope
from idb.utils import snakify, camelify, camelify_feature

app = Flask(__name__)


INVENTORY_QUERY_SCHEMA = {
    "type": "object",
    "properties": {
        "nSamples": {
            "oneOf": [
                {"type": "integer"},
                {"type": "null"}
            ]
        },
        "studyAreaId": {
            "oneOf": [
                {"type": "integer"},
                {"type": "null"}
            ]
        },
        "speciesId": {
            "oneOf": [
                {"type": "integer"},
                {"type": "null"}
            ]
        },
        "isInterpreted": {
            "oneOf": [
                {"type": "boolean"},
                {"type": "null"}
            ]
        }
    },
    "additionalProperties": False
}


FEATURE_SCHEMA = {
    "type": "object",
    "properties": {
        "type": {"type": "string"},
        "properties": {
            "type": "object",
            "properties": {
                "inventoryId": {"type": "integer"},
                "speciesId": {"type": "integer"}
            },
            "required": ["inventoryId", "speciesId"],
            "additionalProperties": False,
        },
        "geometry": {
            "type": "object",
            "properties": {
                "type": {"type": "string", "enum": ["Polygon"]},
                "coordinates": {"type": "array"}
            },
            "required": ["type", "coordinates"]
        },
    },
    "required": ["properties", "geometry"]
}


UPDATE_INVENTORY_SCHEMA = {
    "type": "object",
    "properties": {
        "isInterpreted": {"type": "boolean"}
    },
    "required": ["isInterpreted"],
    "additionalProperties": False
}


@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify( { 'error': 'Bad request' } ), 400)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)


@app.route('/idrop/v0/species', methods = ['GET'])
def get_species():
    with session_scope() as session:
        return jsonify({'species': idb.species(session)})


@app.route('/idrop/v0/studyareas', methods = ['GET'])
def get_studyareas():
    with session_scope() as session:
        return jsonify(idb.studyareas(session))


@app.route('/idrop/v0/studyareas/<int:id>', methods = ['GET'])
def get_studyarea(id):
    with session_scope() as session:
        obj = idb.studyarea(session=session, id=id)
        if obj is None:
            abort(404)
        return jsonify(camelify_feature(obj))


@app.route('/idrop/v0/inventories', methods = ['GET'])
def get_inventories():
    with session_scope() as session:
        fc = idb.inventories(session=session)
    # Camelify properties of feature collection
    fc['features'] = [camelify_feature(f) for f in fc['features']]
    return jsonify(fc)


@app.route('/idrop/v0/inventories', methods = ['POST'])
def get_inventories_filter():
    content = request.get_json(silent=True)
    with session_scope() as session:
        if content is None:
            # Use default parameters
            fc = idb.inventories(session=session)
        else:
            try:
                validate(content, INVENTORY_QUERY_SCHEMA)
            except Exception as e:
                abort(400)
            # Convert camelCase dict keys to snake_case
            params = {snakify(k):v for k,v in content.items()}
            fc = idb.inventories(session=session, **params)
    # Camelify properties of feature collection
    fc['features'] = [camelify_feature(f) for f in fc['features']]
    return jsonify(fc)


@app.route('/idrop/v0/inventories/<int:id>', methods = ['GET'])
def get_inventory(id):
    with session_scope() as session:
        obj = idb.inventory(session=session, id=id)
        if obj is None:
            abort(404)
        return jsonify(camelify_feature(obj))


@app.route('/idrop/v0/interpreted', methods = ['POST'])
def post_interpreted():
    content = request.get_json(silent=True)
    # validate against polygon schema
    if content is None:
        abort(400)
    try:
        validate(content, FEATURE_SCHEMA)
    except Exception as e:
        abort(400)
    feature = content
    feature['properties'] = {snakify(k):v for k,v in
                             feature['properties'].items()}
    with session_scope() as session:
        # add_interpreted returns a list, hence the s
        inserted_features = idb.add_interpreted(session=session, fc=feature)
        # Change the status of is_interpreted in Inventory table to True
        idb.update_inventory(session=session, id=feature['properties']['inventory_id'],
                         is_interpreted=True)
    return jsonify({'interpretedId': inserted_features[0]['properties']['id']}), 201


@app.route('/idrop/v0/interpreted/<int:id>', methods = ['GET'])
def interpreted_by_id(id):
    with session_scope() as session:
        obj = idb.interpreted_by_id(session=session, id=id)
        if obj is None:
            abort(404)
        return jsonify(camelify_feature(obj))


@app.route('/idrop/v0/interpreted', methods = ['GET'])
def get_interpreted():
    with session_scope() as session:
        fc = idb.interpreted(session=session)
    fc['features'] = [camelify_feature(f) for f in fc['features']]
    return jsonify(fc)


@app.route('/idrop/v0/interpreted/filter', methods = ['POST'])
def get_interpreted_filter():
    content = request.get_json(silent=True)
    with session_scope() as session:
        if content is None:
            # Use default parameters
            fc = idb.interpreted(session=session)
        else:
            params = {snakify(k):v for k,v in content.items()}
            fc = idb.interpreted(session=session, **params)
    fc['features'] = [camelify_feature(f) for f in fc['features']]
    return jsonify(fc)


@app.route('/idrop/v0/inventories/<int:id>', methods = ['PATCH'])
def update_inventory_2(id):
    content = request.get_json(silent=True)
    if content is None:
        abort(400)
    try:
        validate(content, UPDATE_INVENTORY_SCHEMA)
    except Exception as e:
        abort(400)
    params = {snakify(k):v for k,v in content.items()}
    params.update(id=id)
    with session_scope() as session:
        updated = idb.update_inventory(session=session, **params)
    if updated == 0:
        abort(400)
    return jsonify({camelify(k):v for k,v in params.items()})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
