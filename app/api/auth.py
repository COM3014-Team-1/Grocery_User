import re
from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash
import jwt

from app.extensions import db, limiter
from app.infrastructure.models.user import User

EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")

def is_valid_email(email: str) -> bool:
    return EMAIL_REGEX.fullmatch(email) is not None

def is_valid_password(password: str) -> bool:
    if len(password) < 8:
        return False
    if not re.search(r"(?=.*[A-Z])", password):
        return False
    if not re.search(r"(?=.*[a-z])", password):
        return False
    if not re.search(r"(?=.*\d)", password):
        return False
    if not re.search(r"(?=.*[^\w\s])", password):
        return False
    return True

failed_logins = {}
LOCKOUT_THRESHOLD = 3
LOCKOUT_DURATION = timedelta(minutes=15)
ATTEMPT_WINDOW = timedelta(minutes=5)

def is_account_locked(identifier: str) -> tuple[bool, str]:
    record = failed_logins.get(identifier)
    now = datetime.utcnow()
    if record and record.get("locked_until") and record["locked_until"] > now:
        remaining = (record["locked_until"] - now).seconds // 60 + 1
        return True, f"Account locked. Try again in {remaining} minutes."
    return False, ""
    return False, ""

def record_failed_attempt(identifier: str):
    now = datetime.utcnow()
    record = failed_logins.get(identifier)
    if record:
        if record["last_attempt"] < now - ATTEMPT_WINDOW:
            record["attempts"] = 1
        else:
            record["attempts"] += 1
        record["last_attempt"] = now
        if record["attempts"] >= LOCKOUT_THRESHOLD:
            record["locked_until"] = now + LOCKOUT_DURATION
    else:
        failed_logins[identifier] = {
            "attempts": 1,
            "last_attempt": now,
            "locked_until": None
        }

def reset_failed_attempts(identifier: str):
    if identifier in failed_logins:
        del failed_logins[identifier]

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/register', methods=['POST'])
@limiter.limit("5 per minute")
def register():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No input data provided"}), 400

    username = data.get('username', '').strip()
    email = data.get('email', '').strip()
    password = data.get('password', '')

    if not username or not email or not password:
        return jsonify({"error": "Missing required fields (username, email, password)"}), 400

    if not is_valid_email(email):
        return jsonify({"error": "Invalid email address"}), 400

    if not is_valid_password(password):
        return jsonify({"error": "Password must be at least 8 characters and contain uppercase, lowercase, digits, and special characters."}), 400

    if User.query.filter((User.username == username) | (User.email == email)).first():
        return jsonify({"error": "User with provided username or email already exists"}), 400

    hashed_password = generate_password_hash(password)
    new_user = User(username=username, email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "message": "User registered successfully",
        "user": {
            "id": new_user.id,
            "username": new_user.username,
            "email": new_user.email
        }
    }), 201

@auth_bp.route('/login', methods=['POST'])
@limiter.limit("5 per minute")
def login():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No input data provided"}), 400

    identifier = data.get('username') or data.get('email', '').strip()
    password = data.get('password', '')

    if not identifier or not password:
        return jsonify({"error": "Missing required fields (identifier and password)"}), 400

    locked, message = is_account_locked(identifier)
    if locked:
        return jsonify({"error": message}), 403

    user = User.query.filter((User.username == identifier) | (User.email == identifier)).first()
    if not user or not check_password_hash(user.password, password):
        record_failed_attempt(identifier)
        return jsonify({"error": "Invalid credentials"}), 401

    reset_failed_attempts(identifier)

    secret = current_app.config.get("SECRET_KEY")
    if not secret:
        return jsonify({"error": "Server configuration error: SECRET_KEY not set"}), 500

    token = jwt.encode({
        'user_id': user.id,
        'exp': datetime.utcnow() + timedelta(hours=1)
    }, secret, algorithm="HS256")

    return jsonify({
        "message": "Login successful",
        "token": token,
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email
        }
    }), 200



# get_user API to retrieve user info
@auth_bp.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    # Retrieve the user based on the provided user_id
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email
    }), 200