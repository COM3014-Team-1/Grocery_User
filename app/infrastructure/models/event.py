# app/infrastructure/models/event.py
from datetime import datetime
from app.extensions import db

class SignUpEvent(db.Model):
    __tablename__ = "signup_events"  # Use a non-reserved table name
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<SignUpEvent user_id={self.user_id} timestamp={self.timestamp}>"

class LoginEvent(db.Model):
    __tablename__ = "login_events"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    success = db.Column(db.Boolean, nullable=False)  # Record whether login succeeded

    def __repr__(self):
        return f"<LoginEvent user_id={self.user_id} success={self.success} timestamp={self.timestamp}>"
