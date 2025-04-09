# app/infrastructure/models/event.py
from datetime import datetime
from app.extensions import db

class SignUpEvent(db.Model):
    __tablename__ = "signup_events"
    id = db.Column(db.Integer, primary_key=True)
    # Update the foreign key reference to point to user.user_id
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<SignUpEvent user_id={self.user_id} timestamp={self.timestamp}>"

class LoginEvent(db.Model):
    __tablename__ = "login_events"
    id = db.Column(db.Integer, primary_key=True)
    # Update the foreign key reference to point to user.user_id
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    success = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f"<LoginEvent user_id={self.user_id} success={self.success} timestamp={self.timestamp}>"

