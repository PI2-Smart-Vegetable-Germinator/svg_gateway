import os

from flask import Blueprint
from flask import jsonify

import requests


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
    response = requests.get('%s/api/planting-time' % os.getenv('SVG_MONITORING_BASE_URI'))

    return jsonify(response.json()), 200

