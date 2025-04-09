import os

import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your-very-secret-key')
    # Update the URL with new PostgreSQL user "htetaung" and database "user_profiles"
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://htetaung:1131992Ha@localhost:5432/user_profiles')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


