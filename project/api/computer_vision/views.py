import os

from flask import Blueprint
from flask import jsonify
from flask_cors import CORS

import requests

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
    response = requests.post('%s/api/submit_image', os.getenv('SVG_COMPUTER_VISION_BASE_URI'), files = {'file': image_file})

    return jsonify(response.json()), response.status_code
