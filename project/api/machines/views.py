from flask import Blueprint
from flask import jsonify
from flask_cors import CORS
from flask import request

from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity

import os
import requests
from requests.exceptions import RequestException
import json

machines_blueprint = Blueprint('machines', __name__)
CORS(machines_blueprint)


@machines_blueprint.route('/api/ping_rasp')
def ping_rasp():
    try:
        requests.get('%s/api/ping' % os.getenv('SVG_RASP_GATEWAY_BASE_URI'))
        return jsonify({'success': True}), 200
    except RequestException:
        return jsonify({'success': False}), 503


@machines_blueprint.route('/api/machine', methods=['POST'])
def update_or_create_machine():
    rasp_ip = request.remote_addr

    post_data = request.get_json()
    post_data['raspberry_ip'] = rasp_ip

    response = requests.post('%s/api/machine' %
                             os.getenv('SVG_MONITORING_BASE_URI'), json=post_data)

    print(response)

    return jsonify(response.json()), response.status_code


@machines_blueprint.route('/api/confirm_pairing', methods=['POST'])
@jwt_required
def confirm_pairing():
    post_data = request.get_json()

    monitoring_response = requests.post(
        '%s/api/confirm_pairing' % os.getenv('SVG_MONITORING_BASE_URI'), json=post_data)

    if monitoring_response.status_code == 404:
        return jsonify(monitoring_response.json()), 404

    monitoring_response_json = monitoring_response.json()
    user_id = get_jwt_identity()
    machine_id = monitoring_response_json['machineId']

    auth_service_data = {
        'userId': user_id,
        'machineId': machine_id
    }

    auth_response = requests.put(
        '%s/api/pairing' % os.getenv('SVG_AUTH_BASE_URI'), json=auth_service_data)

    if auth_response.status_code != 200:
        return jsonify({
            'success': False,
            'message': 'Could not pair machine to user'
        }), 400

    rasp_response = requests.get(
        '%s/api/confirm_pairing' % os.getenv('SVG_RASP_GATEWAY_BASE_URI'))

    if rasp_response.status_code != 200:
        return jsonify({
            'success': False,
            'message': 'Could not pair machine to user'
        }), 400

    return jsonify({
        'success': True,
        'machineId': machine_id
    }), 201


@machines_blueprint.route('/api/start_planting', methods=['POST'])
def start_planting():
    post_data = request.get_json()

    monitoring_response = requests.post(
        '%s/api/planting' % os.getenv('SVG_MONITORING_BASE_URI'), json=post_data)

    return jsonify(monitoring_response.json()), monitoring_response.status_code


@machines_blueprint.route('/api/end_planting', methods=['POST'])
def end_planting():
    post_data = request.get_json()

    monitoring_response = requests.post(
        '%s/api/end_planting' % os.getenv('SVG_MONITORING_BASE_URI'), json=post_data)

    return jsonify(monitoring_response.json()), monitoring_response.status_code


@machines_blueprint.route('/api/update_planting_info', methods=['POST'])
def update_planting_info():

    post_data = request.get_json()

    monitoring_response = requests.post(
        '%s/api/update_planting_info' % os.getenv('SVG_MONITORING_BASE_URI'), json=post_data)

    if monitoring_response.status_code != 201:
        return jsonify({
            'success': False,
            'message': 'Error updating info'
        }), 400

    return jsonify({
        'success': True,
    }), 201


# SECTION IRRIGATION --------------------------------------------------

@machines_blueprint.route('/api/start_irrigation', methods=['POST'])
def start_irrigation():
    post_data = request.get_json()

    monitoring_response = requests.post(
        '%s/api/start_irrigation' % os.getenv('SVG_MONITORING_BASE_URI'), json=post_data)

    return jsonify(monitoring_response.json()), monitoring_response.status_code


@machines_blueprint.route('/api/app/start_irrigation', methods=['POST'])
def app_start_irrigation():
    post_data = request.get_json()

    rasp_response = requests.get(
        '%s/api/app/start_irrigation' % os.getenv('SVG_RASP_GATEWAY_BASE_URI'))

    print(rasp_response.content)

    if rasp_response.status_code != 200:
        return jsonify({
            'success': False,
            'message': 'Irrigation error'
        }), 400

    monitoring_response = requests.post(
        '%s/api/start_irrigation' % os.getenv('SVG_MONITORING_BASE_URI'), json=post_data)

    return jsonify(monitoring_response.json()), monitoring_response.status_code


@machines_blueprint.route('/api/end_irrigation', methods=['POST'])
def end_irrigation():
    post_data = request.get_json()

    monitoring_response = requests.post(
        '%s/api/end_irrigation' % os.getenv('SVG_MONITORING_BASE_URI'), json=post_data)

    return jsonify(monitoring_response.json()), monitoring_response.status_code


@machines_blueprint.route('/api/app/switch_smart_irrigation',  methods=['POST'])
@jwt_required
def app_switch_smart_irrigation():
    user_id = get_jwt_identity()

    responseAuth = requests.get(os.getenv('SVG_AUTH_BASE_URI') + f'/api/user/{user_id}', )

    response_data = responseAuth.json()
    machine_id = response_data['machineId']

    responseMonitoring = requests.post(os.getenv('SVG_MONITORING_BASE_URI') + f'/api/switch_smart_irrigation/{machine_id}', )
    monitoringJson = responseMonitoring.json()
    responseRaspgate = requests.post(os.getenv('SVG_RASP_GATEWAY_BASE_URI') + f'/api/toggle_smart_irrigation', json={'smartIrrigationEnabled': monitoringJson.get('smart_irrigation_status')})

    return jsonify(responseMonitoring.json()), 200
    

@machines_blueprint.route('/api/app/get_smart_irrigation_status',  methods=['GET'])
@jwt_required
def get_smart_irrigation_status():
    user_id = get_jwt_identity()

    responseAuth = requests.get(os.getenv('SVG_AUTH_BASE_URI') + f'/api/user/{user_id}', )

    response_data = responseAuth.json()
    machine_id = response_data['machineId']

    responseMonitoring = requests.get(os.getenv('SVG_MONITORING_BASE_URI') + f'/api/get_smart_irrigation_status/{machine_id}', )

    return jsonify(responseMonitoring.json()), 200

# SECTION ILLUMINATION --------------------------------------------------

@machines_blueprint.route('/api/switch_illumination', methods=['POST'])
def switch_illumination():
    post_data = request.get_json()
    currently_backlit = post_data['currently_backlit']

    if currently_backlit:
        # print('start_illumination')
        monitoring_response = requests.post(
            '%s/api/start_illumination' % os.getenv('SVG_MONITORING_BASE_URI'), json=post_data)

        return jsonify(monitoring_response.json()), monitoring_response.status_code

    else:
        # print('end_illumination')
        monitoring_response = requests.post(
            '%s/api/end_illumination' % os.getenv('SVG_MONITORING_BASE_URI'), json=post_data)

        return jsonify(monitoring_response.json()), monitoring_response.status_code


@machines_blueprint.route('/api/app/switch_illumination', methods=['POST'])
def app_switch_illumination():
    post_data = request.get_json()

    rasp_response = requests.get(
        '%s/api/app/switch_illumination' % os.getenv('SVG_RASP_GATEWAY_BASE_URI'))

    if rasp_response.status_code != 200:
        return jsonify({
            'success': False,
            'message': 'Illumination error'
        }), 400

    rasp_response_data = rasp_response.json()
    currently_backlit = rasp_response_data['currently_backlit']

    if currently_backlit:
        # print('start_illumination')
        monitoring_response = requests.post(
            '%s/api/start_illumination' % os.getenv('SVG_MONITORING_BASE_URI'), json=post_data)

        return jsonify(monitoring_response.json()), monitoring_response.status_code

    else:
        print('end_illumination')
        monitoring_response = requests.post(
            '%s/api/end_illumination' % os.getenv('SVG_MONITORING_BASE_URI'), json=post_data)

        return jsonify(monitoring_response.json()), monitoring_response.status_code

