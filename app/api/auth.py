import re
from datetime import datetime, timedelta
from flask.views import MethodView
from flask_smorest import Blueprint, abort
import jwt
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash

from app.extensions import db, limiter
from app.infrastructure.models.user import User
from app.schemas.register import RegisterSchema
from app.schemas.login import LoginSchema
from app.schemas.user import UserSchema

# Regular expression for email validation
EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")

def is_valid_email(email: str) -> bool:
    return bool(EMAIL_REGEX.fullmatch(email))

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
        failed_logins[identifier] = {"attempts": 1, "last_attempt": now, "locked_until": None}

def reset_failed_attempts(identifier: str):
    failed_logins.pop(identifier, None)

# Initialize the Flask-Smorest blueprint
blueprint = Blueprint("auth", "auth", url_prefix="/api/auth", description="Authentication routes")

# -------------------------
# Registration API
# -------------------------
@blueprint.route("/register")
class RegisterResource(MethodView):
    decorators = [limiter.limit("5 per minute")]

    @blueprint.arguments(RegisterSchema, location="json")
    @blueprint.response(201, UserSchema)
    def post(self, data):
        # Map incoming fields (using "username" as input, mapped to User.name)
        name = data.get("username", "").strip()
        email = data.get("email", "").strip()
        password = data.get("password", "")
        phone = data.get("phone", "").strip()
        address = data.get("address", "").strip()
        city = data.get("city", "").strip()
        state = data.get("state", "").strip()
        zipcode = data.get("zipcode", "").strip()

        # Validate required fields
        if not name or not email or not password:
            abort(400, message="Missing required fields (username, email, password).")
        if not is_valid_email(email):
            abort(400, message="Invalid email.")
        if not is_valid_password(password):
            abort(400, message="Weak password.")
        if User.query.filter((User.name == name) | (User.email == email)).first():
            abort(400, message="Username or email already taken.")

        hashed_password = generate_password_hash(password)
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
                "created_at": new_user.created_at.isoformat()
            }
        }
    
# -------------------------
# Login API
# -------------------------
@blueprint.route("/login")
class LoginResource(MethodView):
    decorators = [limiter.limit("5 per minute")]

    @blueprint.arguments(LoginSchema, location="json")
    @blueprint.response(200)
    def post(self, data):
        identifier = data.get("identifier", "").strip()
        password = data.get("password", "")

        if not identifier or not password:
            abort(400, message="Missing credentials.")

        locked, message = is_account_locked(identifier)
        if locked:
            abort(403, message=message)

        user = User.query.filter((User.name == identifier) | (User.email == identifier)).first()
        if not user or not check_password_hash(user.password_hash, password):
            record_failed_attempt(identifier)
            abort(401, message="Invalid credentials.")
        reset_failed_attempts(identifier)

        secret = current_app.config.get("SECRET_KEY")
        if not secret:
            abort(500, message="Server configuration error.")

        token = jwt.encode({
            "user_id": user.user_id,
            "exp": datetime.utcnow() + timedelta(hours=1)
        }, secret, algorithm="HS256")

        return {
            "message": "Login successful.",
            "token": token,
            "user": {
                "user_id": user.user_id,
                "name": user.name,
                "email": user.email,
                "phone": user.phone,
                "address": user.address,
                "city": user.city,
                "state": user.state,
                "zipcode": user.zipcode,
                "created_at": user.created_at.isoformat()
            }
        }
    
# -------------------------
# Get User Info API
# -------------------------
@blueprint.route("/user/<int:user_id>")
class UserResource(MethodView):
    @blueprint.response(200, UserSchema)
    def get(self, user_id):
        user = User.query.get(user_id)
        if not user:
            abort(404, message="User not found.")
        return user