#!/usr/bin/env python3

from flask import Flask, jsonify, abort, request, make_response, url_for
from jsonschema import validate

import idb
from idb.db import session_scope

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


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
