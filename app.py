#!/usr/bin/env python3

from flask import Flask, jsonify, abort, request, make_response, url_for
from jsonschema import validate

import idb
from idb.db import session_scope
from idb.utils import snakify, camelify_feature

app = Flask(__name__)


INVENTORY_QUERY_SCHEMA = {
    "type": "object",
    "properties": {
        "nSamples": {"type": "integer"},
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
        }
    },
    "required": ["nSamples"],
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
        return jsonify({'species': idb.studyareas(session)})


@app.route('/idrop/v0/inventories', methods = ['GET'])
def get_inventories():
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
    return jsonify({'interpretedId': inserted_features[0]['properties']['id']}), 201


@app.route('/idrop/v0/interpreted', methods = ['GET'])
def get_interpreted():
    content = request.get_json(silent=True)
    with session_scope() as session:
        if content is None:
            # Use default parameters
            fc = idb.interpreted(session=session)
        else:
            params = {snakify(k):v for k,v in content.items()}
            fc = idb.interpreted(session=session, **params)
    return jsonify(fc)


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
