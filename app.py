#!/usr/bin/env python3

from flask import Flask, jsonify, abort, request, make_response, url_for
from jsonschema import validate

import idb
from idb.db import session_scope
from idb.utils import snakify

app = Flask(__name__)


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
        # Convert camelCase dict keys to snake_case
        params = {snakify(k):v for k,v in content.items()}
        # TODO: Implement json validation
        # try:
            # validate(content, SEARCH_SCHEMA)
        # except Exception as e:
            # abort(400)
        fc = idb.inventories(session=session, **params)
    return jsonify(fc)


@app.route('/idrop/v0/interpreted', methods=['POST'])
def post_interpreted():
    content = request.get_json(silent=True)
    # TODO: implement proper json validation
    if content is None:
        abort(400)
    feature = {snakify(k):v for k,v in content.items()}
    with session_scope() as session:
        # add_interpreted returns a list, hence the s
        inserted_features = idb.add_interpreted(session=session, fc=feature)
    return jsonify({'interpretedId': inserted_features[0]['id']}), 201


@app.route('/idrop/v0/interpreted', method=['GET'])
def get_interpreted():
    content = request.get_json(silent=True)
    with session_scope() as session:
        if content is None:
            # Use default parameters
            fc = idb.interpreted(session=session)
        params = {snakify(k):v for k,v in content.items()}
        fc = idb.interpreted(session=session, **params)
    return jsonify(fc)




if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
