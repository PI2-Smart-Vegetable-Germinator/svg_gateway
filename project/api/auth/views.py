import os

from flask import Blueprint
from flask import jsonify
from flask import request

import requests

from .utils import generate_auth_tokens


auth_blueprint = Blueprint('auth', __name__)


@auth_blueprint.route('/api/ping', methods=['GET'])
def ping():
    return jsonify({
        'response': 'pong!'
    }), 200


@auth_blueprint.route('/api/auth_ping', methods=['GET'])
def auth_ping():
    response = requests.get('%s/api/ping' % os.getenv('SVG_AUTH_BASE_URI'))

    return jsonify(response.json()), 200
    

@auth_blueprint.route('/api/planting-time/', methods=['GET'])
def get_planting_time():
    response = requests.get('%s/api/planting-time' % os.getenv('SVG_MONITORING_BASE_URI'), json=request.get_json())

    return jsonify(response.json()), 200


@auth_blueprint.route('/api/signup', methods=['POST'])
def signup():
    response = requests.post('%s/api/signup' % os.getenv('SVG_AUTH_BASE_URI'), json=request.get_json())
    response_data = response.json()

    if response.status_code == 201:
        return jsonify({
            'status': 'success',
            'authTokens': generate_auth_tokens(response_data['userId'])
        }), 201

    return jsonify(response_data), response.status_code


@auth_blueprint.route('/api/login', methods=['POST'])
def login():
    response = requests.post('%s/api/login' % os.getenv('SVG_AUTH_BASE_URI'), json=request.get_json())
    response_data = response.json()

    if response.status_code == 201:
        return jsonify({
            'status': 'success',
            'authTokens': generate_auth_tokens(response_data['userId'])
        }), 201

    return jsonify(response_data), response.status_code
