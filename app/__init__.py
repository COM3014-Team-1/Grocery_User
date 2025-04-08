from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Initialize the database and migration extensions
db = SQLAlchemy()
migrate = Migrate()
limiter = Limiter(key_func=get_remote_address)

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    # Initialize the extensions with the app instance
    db.init_app(app)
    migrate.init_app(app, db)
    limiter.init_app(app)

    # Import the User model to ensure it's loaded for migration detection
    from app.infrastructure.models.user import User

    # Import and register the authentication blueprint
    from app.api.auth import auth_bp
    app.register_blueprint(auth_bp)

    return app

