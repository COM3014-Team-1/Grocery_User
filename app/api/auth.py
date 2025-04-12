import re
from datetime import datetime, timedelta
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask import request, current_app, jsonify
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

# Brute-force lockout logic
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

# --------------------------------------
# ✅ Flask-Smorest Blueprint
# --------------------------------------
blueprint = Blueprint("auth", "auth", url_prefix="/api/auth", description="Authentication routes")

# --------------------------------------
# 📌 Updated Register API including created_at field
# --------------------------------------
@blueprint.route("/register")
class RegisterResource(MethodView):
    decorators = [limiter.limit("5 per minute")]

    @blueprint.arguments(dict, location="json")
    @blueprint.response(201)
    def post(self, data):
        # Extract and clean fields from the incoming JSON data.
        name = data.get("username", "").strip()  # Mapping 'username' field to the 'name' attribute in the model.
        email = data.get("email", "").strip()
        password = data.get("password", "")
        phone = data.get("phone", "").strip()
        address = data.get("address", "").strip()
        city = data.get("city", "").strip()
        state = data.get("state", "").strip()
        zipcode = data.get("zipcode", "").strip()

        # Check required fields.
        if not name or not email or not password:
            abort(400, message="Missing required fields (username, email, password).")

        if not is_valid_email(email):
            abort(400, message="Invalid email.")

        if not is_valid_password(password):
            abort(400, message="Weak password.")

        if User.query.filter((User.name == name) | (User.email == email)).first():
            abort(400, message="Username or email already taken.")

        # Hash the password.
        hashed_password = generate_password_hash(password)
        
        # Create a new user record. Note: created_at is automatically set via the default in the model.
        new_user = User(
            name=name,
            email=email,
            password_hash=hashed_password,
            phone=phone,
            address=address,
            city=city,
            state=state,
            zipcode=zipcode
        )

        db.session.add(new_user)
        db.session.commit()

        # Return the created user info, including the created_at timestamp.
        return {
            "message": "User registered successfully.",
            "user": {
                "user_id": new_user.user_id,
                "name": new_user.name,
                "email": new_user.email,
                "phone": new_user.phone,
                "address": new_user.address,
                "city": new_user.city,
                "state": new_user.state,
                "zipcode": new_user.zipcode,
                "created_at": new_user.created_at.isoformat()  # Format datetime as an ISO string.
            }
        }
