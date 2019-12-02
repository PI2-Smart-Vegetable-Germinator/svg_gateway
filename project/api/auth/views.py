import os

from flask import Blueprint, jsonify, request, send_file

from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity

import requests

from .utils import generate_auth_tokens

import sys

auth_blueprint = Blueprint('auth', __name__)


@auth_blueprint.route('/api/ping', methods=['GET'])
def ping():
    return jsonify({
        'response': 'pong!'
    }), 200


@auth_blueprint.route('/api/auth_ping', methods=['GET'])
def auth_ping():
    response = requests.get('%s/api/ping' % os.getenv('SVG_COMPUTER_VISION_BASE_URI'))

    return jsonify(response.json()), 200


@auth_blueprint.route('/api/current-info', methods=['GET'])
@jwt_required
def get_current_info():

    user_id = get_jwt_identity()

    responseAuth = requests.get(os.getenv('SVG_AUTH_BASE_URI') + f'/api/user/{user_id}', json=request.get_json())

    response_data = responseAuth.json()
    machine_id = response_data['machineId']

    responseMonitoring = requests.get(os.getenv('SVG_MONITORING_BASE_URI') + f'/api/current-info/{machine_id}/', json=request.get_json())

    return jsonify(responseMonitoring.json()), 200


@auth_blueprint.route('/api/plantings-history', methods=['GET'])
@jwt_required
def get_plantings_history():

    user_id = get_jwt_identity()

    responseAuth = requests.get(os.getenv('SVG_AUTH_BASE_URI') + f'/api/user/{user_id}', json=request.get_json())

    response_data = responseAuth.json()
    machine_id = response_data['machineId']

    responseMonitoring = requests.get(os.getenv('SVG_MONITORING_BASE_URI') + f'/api/plantings-history/{machine_id}/', json=request.get_json())

    return jsonify(responseMonitoring.json()), 200


@auth_blueprint.route('/api/signup', methods=['POST'])
def signup():
    response = requests.post(
        '%s/api/signup' % os.getenv('SVG_AUTH_BASE_URI'), json=request.get_json())
    response_data = response.json()

    if response.status_code == 201:
        return jsonify({
            'status': 'success',
            'authTokens': generate_auth_tokens(response_data['userId'])
        }), 201

    return jsonify(response_data), response.status_code


@auth_blueprint.route('/api/login', methods=['POST'])
def login():
    response = requests.post(
        '%s/api/login' % os.getenv('SVG_AUTH_BASE_URI'), json=request.get_json())
    response_data = response.json()

    if response.status_code == 201:
        return jsonify({
            'status': 'success',
            'authTokens': generate_auth_tokens(response_data['userId'])
        }), 201

    return jsonify(response_data), response.status_code


@auth_blueprint.route('/api/users', methods=['GET'])
def users():
    response = requests.get('%s/api/users' % os.getenv('SVG_AUTH_BASE_URI'), json=request.get_json())
    response_data = response.json()

    return jsonify(response_data), response.status_code


@auth_blueprint.route('/api/get_user', methods=['GET'])
@jwt_required
def get_user():
    user_id = get_jwt_identity()

    response = requests.get('%s/api/users/%s' % (os.getenv('SVG_AUTH_BASE_URI'), user_id))
    response_data = response.json()

    return jsonify(response_data), response.status_code


@auth_blueprint.route('/api/device_id', methods=['POST'])
@jwt_required
def update_device_id():
    post_data = request.get_json()
    user_id = get_jwt_identity()

    post_data['userId'] = user_id

    print(post_data)

    response = requests.post('%s/api/device_id' % os.getenv('SVG_AUTH_BASE_URI'), json=post_data)
    response_data = response.json()

    return jsonify(response_data), response.status_code


@auth_blueprint.route('/api/get-image', methods=['GET'])
@jwt_required
def get_image():
    user_id = get_jwt_identity()

    responseAuth = requests.get(os.getenv('SVG_AUTH_BASE_URI') + f'/api/user/{user_id}', json=request.get_json())

    response_data = responseAuth.json()
    machine_id = response_data['machineId']

    monitor_response = requests.get('%s/api/current-info/%s' % (os.getenv('SVG_MONITORING_BASE_URI'), machine_id))
    monitor_data = monitor_response.json()

    planting_id = monitor_data.get('data').get('planting_id')

    post_data = { "machine_id": planting_id }
    response = requests.post('%s/api/get-image' % os.getenv('SVG_COMPUTER_VISION_BASE_URI'), json=post_data)

    return response.content, response.status_code
