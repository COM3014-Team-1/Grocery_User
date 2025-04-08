import os

class Config:
    # Ensure you set a SECRET_KEY in your environment or use the default for development.
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your-very-secret-key')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Use DATABASE_URL if defined, otherwise fallback to a local setup.
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://postgres:password@localhost:5432/Grocery_User')
