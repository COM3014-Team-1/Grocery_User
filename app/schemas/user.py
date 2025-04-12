from marshmallow import Schema, fields

class UserSchema(Schema):
    user_id = fields.Int(dump_only=True, description="User primary key")
    username = fields.Str(dump_only=True, attribute="name", description="User's full name")
    email = fields.Email(dump_only=True, description="User's email address")
    phone = fields.Str(dump_only=True, description="User's phone number")
    address = fields.Str(dump_only=True, description="User's address")
    city = fields.Str(dump_only=True, description="User's city")
    state = fields.Str(dump_only=True, description="User's state")
    zipcode = fields.Str(dump_only=True, description="User's zipcode")
    created_at = fields.DateTime(dump_only=True, description="Timestamp when the user was created")
    updated_at = fields.DateTime(dump_only=True, description="Timestamp when the user was last updated")
    last_login = fields.DateTime(dump_only=True, description="Timestamp of the user's last login")