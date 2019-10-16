from flask import Blueprint
from flask import jsonify
from flask_cors import CORS
from flask import request

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