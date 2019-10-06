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
