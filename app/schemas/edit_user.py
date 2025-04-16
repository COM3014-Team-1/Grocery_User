#app>shemas>edit_user.py
from marshmallow import Schema, fields

class EditUserSchema(Schema):
    username = fields.Str(required=False, description="User's full name")
    email = fields.Email(required=False, description="User's email address")
    phone = fields.Str(required=False, description="User's phone number")
    address = fields.Str(required=False, description="User's address")
    city = fields.Str(required=False, description="User's city")
    state = fields.Str(required=False, description="User's state")
    zipcode = fields.Str(required=False, description="User's zipcode")
    created_at = fields.DateTime(required=False, missing=None, description="User's account creation date")
    updated_at = fields.DateTime(required=False, missing=None, description="User's account update date")
    last_login = fields.DateTime(required=False, missing=None, description="User's last login date")