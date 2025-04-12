from flask import Flask
from flask_smorest import Api
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
import pkgutil
import importlib

from app.config import Config
from app.extensions import db, migrate, limiter

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Enable CORS globally
    CORS(app)

    # Initialize core extensions
    db.init_app(app)
    migrate.init_app(app, db)
    limiter.init_app(app)

    # --- Flask-Smorest API Config ---
    app.config.update({
        "API_TITLE": "User Microservice",
        "API_VERSION": "v1",
        "OPENAPI_VERSION": "3.0.2",
        "OPENAPI_URL_PREFIX": "/",
        "OPENAPI_JSON_PATH": "openapi.json",
    })

    api = Api(app)

    # Import all models so Flask-Migrate picks them up
    from app.infrastructure.models.user import User
    from app.infrastructure.models.event import SignUpEvent, LoginEvent

    # Automatically discover and register blueprints in app/api/
    for _, module_name, _ in pkgutil.iter_modules(["app/api"]):
        module = importlib.import_module(f"app.api.{module_name}")
        if hasattr(module, "blueprint"):
            api.register_blueprint(module.blueprint)
            print(f"✔ Registered blueprint: {module_name}")

    # Swagger UI Setup
    swagger_ui_url = "/swagger"
    openapi_json_url = "/openapi.json"

    swaggerui_blueprint = get_swaggerui_blueprint(
        swagger_ui_url,
        openapi_json_url,
        config={"app_name": "User Microservice"}
    )
    app.register_blueprint(swaggerui_blueprint, url_prefix=swagger_ui_url)

    return app




