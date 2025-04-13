from flask import Blueprint, request, jsonify
import bcrypt
from Model.Database.conn import insert_user

register_bp = Blueprint('register', __name__)

@register_bp.route('/register', methods=['POST'])
def register():
    """Regisztrációt kezeli"""

    username = request.json.get('username')
    email = request.json.get('email')
    password = request.json.get('password')
    age = request.json.get('age')

    if not username or not email or not password or not age:
        return jsonify({"error": "Missing required fields"}), 400

    hashed_password = hash_password(password)

    if insert_user(username, email, hashed_password, age, "prod"):
        return jsonify({"message": "User registered successfully"}), 200
    else:
        return jsonify({"error": "Username or email already exists"}), 401


def hash_password(password):
    """Hasheli a jelszót a titkosítás érdekében"""
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')