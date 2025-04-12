from marshmallow import Schema, fields

class RegisterSchema(Schema):
    username = fields.Str(required=True, description="User's full name")
    email = fields.Email(required=True, description="User's email address")
    password = fields.Str(required=True, description="User's password")
    phone = fields.Str(required=False, description="User's phone number")
    address = fields.Str(required=False, description="User's street address")
    city = fields.Str(required=False, description="City of residence")
    state = fields.Str(required=False, description="State of residence")
    zipcode = fields.Str(required=False, description="Zip or postal code")
