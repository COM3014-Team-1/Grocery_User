import os

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:password@localhost:5432/Grocery_User'
    #setting db parameter from command lines
    #SQLALCHEMY_DATABASE_URI = f"postgresql://{os.getenv('DB_USER')}:os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"