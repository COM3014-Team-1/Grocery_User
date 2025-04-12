
from marshmallow import Schema, fields, validate, ValidationError

class RegisterSchema(Schema):
    username = fields.Str(
        required=True, 
        validate=validate.Length(min=1),
        description="User's full name"
    )
    email = fields.Email(
        required=True,
        description="User's email address"
    )
    password = fields.Str(
        required=True,
        validate=validate.Length(min=8),
        description="User's password"
    )
    phone = fields.Str(
        required=True,
        description="User's phone number"
    )
    address = fields.Str(
        required=True,
        description="User's address"
    )
    city = fields.Str(
        required=True,
        description="User's city"
    )
    state = fields.Str(
        required=True,
        description="User's state"
    )
    zipcode = fields.Str(
        required=True,
        description="User's zipcode"
    )
    created_at = fields.DateTime(
        required=False,
        missing=None,
        description="User's account creation date"
    )
    updated_at = fields.DateTime(
        required=False,
        missing=None,
        description="User's account update date"
    )
    last_login = fields.DateTime(
        required=False,
        missing=None,
        description="User's last login date"
    )
    
    # Custom validation for required fields
    def validate_required_fields(self, data):
        if not data.get("username") or not data.get("email") or not data.get("password"):
            raise ValidationError("Missing required fields")