from flask import Blueprint, request, jsonify
from app.application.user.getuser.getuserhandler import get_user_handler

user_bp = Blueprint('user', __name__)

@user_bp.route('/get', methods=['GET'])
def get_user():
    user_id = request.args.get('id')
    if not user_id:
        return jsonify({"error": "User ID is required"}), 400
    
    user_data = get_user_handler(user_id)
    if user_data:
        return jsonify(user_data), 200
    return jsonify({"error": "User not found"}), 404
