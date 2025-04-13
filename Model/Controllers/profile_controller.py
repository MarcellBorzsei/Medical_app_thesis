from flask import Blueprint, request, jsonify
from Model.Database.conn import get_images_by_user, get_user_by_username

profile_bp = Blueprint('profile', __name__)


@profile_bp.route('/pictures', methods=['GET'])
def get_uploaded_images():
    """Profil oldal feltöltött képek lekérését kezeli"""

    id = request.args.get('id')

    if not id:
        return jsonify({"error": "Missing required fields"}), 400

    images_data = get_images_by_user(id, "prod")

    if not images_data:
        return jsonify({"error": "No uploaded images found for this user"}), 401

    return jsonify(images_data), 200

@profile_bp.route('/personal_data', methods=['GET'])
def get_personal_data():
    """Profil oldal személyes adatok lekérését kezeli."""

    username = request.args.get('username')

    if not username:
        return jsonify({"error": "Username is required"}), 400

    data = get_user_by_username(username, "prod")

    if not data:
        return jsonify({"error": "No user found with the given name"}), 401

    personal_data ={
        "username": data[1],
        "email": data[3],
        "age": data[4]
    }

    return jsonify(personal_data), 200