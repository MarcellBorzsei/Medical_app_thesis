from flask import Blueprint, request, jsonify
import bcrypt
from Model.Database.conn import get_user_by_username

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    """Bejelentkezést kezeli"""

    try:
        data = request.json
        if not data or not data.get("username") or not data.get("password"):
            return jsonify({"error": "Username and password required"}), 400
    except Exception as e:
        return jsonify({"error": f"Invalid JSON format: {str(e)}"}), 400

    username = data["username"]
    password = data["password"]

    user = get_user_by_username(username, "prod")

    if user is not None:
        if verify_password(user[2], password):
            return jsonify({"message": "Login successful", "id": user[0] ,"username": user[1]}), 200
        else:
            return jsonify({"error": "Invalid username or password"}), 401
    else:
        return jsonify({"error": "User is not in the database"}), 402


def verify_password(stored_password, provided_password):
    """Leellenőrzi, hogy a tárolt hashelt jelszó és a megadott jelszó egyezik-e."""
    try:
        return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password.encode('utf-8'))
    except Exception as e:
        print(f"Password verification failed: {e}")
        return False