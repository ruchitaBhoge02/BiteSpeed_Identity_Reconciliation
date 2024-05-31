from flask import Blueprint, request, jsonify
from core.handler.identity_handler import identify

identify_route = Blueprint('identify_route', __name__)


@identify_route.route('/identify', methods=['POST'])
def identify_handler():
    try:
        data = request.get_json()
        response = identify(data)
        return jsonify(response), 200
    except Exception as e:
        print(f"Error in identify_handler: {e}")
        return jsonify({"error": "An error occurred while processing your request."}), 500
