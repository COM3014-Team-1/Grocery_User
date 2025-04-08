from flask import Flask
from app.config import Config
from app.extensions import db, migrate, limiter

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    limiter.init_app(app)

    # Import models so migrations detect them
    from app.infrastructure.models.user import User

    # Import blueprints after extensions are initialized
    from app.api.auth import auth_bp
    app.register_blueprint(auth_bp)

    return app



