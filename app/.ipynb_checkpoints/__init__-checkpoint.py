from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Initialize the database and migration extensions
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    # Initialize the extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Import the model to ensure it's loaded for migration detection
    from app.infrastructure.models.user import User  # Import the model
    
    return app
