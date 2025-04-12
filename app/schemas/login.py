from marshmallow import Schema, fields, validate

class LoginSchema(Schema):
    identifier = fields.Str(
        required=True,
        description="Username (full name) or email"
    )
    password = fields.Str(
        required=True,
        validate=validate.Length(min=8),
        description="User's password"
    )
    remember_me = fields.Bool(
        required=False,
        missing=False,
        description="Remember me option"
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
