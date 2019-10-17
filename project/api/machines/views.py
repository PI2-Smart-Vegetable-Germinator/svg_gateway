from flask import Blueprint
from flask import jsonify
from flask_cors import CORS
from flask import request

from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity

import os
import requests
import json

machines_blueprint = Blueprint('machines', __name__)
CORS(machines_blueprint)

@machines_blueprint.route('/api/machine', methods=['POST'])
def update_or_create_machine():
    rasp_ip = request.remote_addr

    post_data = request.get_json()
    post_data['raspberry_ip'] = rasp_ip

    response = requests.post('%s/api/machine' % os.getenv('SVG_MONITORING_BASE_URI'), json=post_data)

    return jsonify(response.json()), response.status_code


@machines_blueprint.route('/api/confirm_pairing', methods=['POST'])
@jwt_required
def confirm_pairing():
    post_data = request.get_json()

    monitoring_response = requests.post('%s/api/confirm_pairing' % os.getenv('SVG_MONITORING_BASE_URI'), json=post_data)

    if monitoring_response.status_code == 404:
        return jsonify(monitoring_response.json()), 404

    monitoring_response_json = monitoring_response.json()
    user_id = get_jwt_identity()
    machine_id = monitoring_response_json['machineId']

    auth_service_data = {
        'userId': user_id,
        'machineId': machine_id
    }

    auth_response = requests.put('%s/api/pairing' % os.getenv('SVG_AUTH_BASE_URI'), json=auth_service_data)

    if auth_response.status_code != 200:
        return jsonify({
            'success': False,
            'message': 'Could not pair machine to user'
        }), 400

    rasp_response = requests.get('%s/api/confirm_pairing' % os.getenv('SVG_RASP_GATEWAY_BASE_URI'))

    if rasp_response.status_code != 200:
        return jsonify({
            'success': False,
            'message': 'Could not pair machine to user'
        }), 400

    return jsonify({
        'success': True
    }), 201
