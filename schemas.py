from marshmallow import Schema, fields, validate

class RegisterSchema(Schema):
    name = fields.String(required=True, validate=validate.Length(min=1))
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=4))

class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)

class BookingSchema(Schema):
    event_id = fields.Integer(required=True)
