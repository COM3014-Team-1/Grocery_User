import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'GT6kS1_ascJ2lv8LvL-QIiXGzsBjJvGmFJri5YmKQU6wBamEn3kVjN4YsyTKBTQlH-vz--tLRi-HqToRuHHWeQ==')
    # Update the URL with new PostgreSQL user "htetaung" and database "user_profiles"
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://postgres:SHMIgtBBk1zQKYhMSmDX@database-1.c3u0oys8ik2c.eu-west-2.rds.amazonaws.com:5432/user_profiles')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


