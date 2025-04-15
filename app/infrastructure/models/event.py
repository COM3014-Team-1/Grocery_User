# app/infrastructure/models/event.py
import uuid
from datetime import datetime
from app.extensions import db
from sqlalchemy.dialects.postgresql import UUID

class SignUpEvent(db.Model):
    __tablename__ = "signup_events"
    # Use UUID for the primary key
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    # Update foreign key to reference the updated users table and its UUID key
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("user.user_id"), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<SignUpEvent user_id={self.user_id} timestamp={self.timestamp}>"

class LoginEvent(db.Model):
    __tablename__ = "login_events"
    # Similarly using UUID for the primary key for the login event model
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("user.user_id"), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    success = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f"<LoginEvent user_id={self.user_id} success={self.success} timestamp={self.timestamp}>"


