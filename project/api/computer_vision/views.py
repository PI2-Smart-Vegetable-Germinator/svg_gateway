import os

from flask import Blueprint
from flask import jsonify
from flask_cors import CORS
from flask import request

import requests
import json

computer_vision_blueprint = Blueprint('computer_vision', __name__)
CORS(computer_vision_blueprint)

@computer_vision_blueprint.route('/api/computer_vision_ping', methods=['GET'])
def computer_vision_ping():
    response = requests.get('%s/api/ping' % os.getenv('SVG_COMPUTER_VISION_BASE_URI'))

    return jsonify(response.json()), 200

@computer_vision_blueprint.route('/api/submit_image', methods=['POST'])
def computer_vision_submit_image():
    if 'file' not in request.files:
        return jsonify({
            'response': 'Image not found!',
        }), 404
    image_file = request.files['file']
    planting_id = request.json['planting_id']
    response = requests.post('%s/api/submit_image' % os.getenv('SVG_COMPUTER_VISION_BASE_URI'), json = planting_id, files = {'file': image_file})

    return jsonify(response.json()), response.status_code

@computer_vision_blueprint.route('/api/trigger_image_capture', methods=['POST'])
def computer_vision_trigger_image_capture():
    url ='http://' + '192.168.0.23' + ':5000/api/take_photo'
    data = {'raspberry_ip': request.json['raspberry_ip'], 'planting_id' : request.json['planting_id']}
    response = requests.post(url, json=data)

    return jsonify(response.json()), response.status_code
