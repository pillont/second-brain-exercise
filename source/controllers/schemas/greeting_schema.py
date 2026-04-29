from marshmallow import Schema, fields


class GreetingSchema(Schema):
    id = fields.Int(required=True)
    message = fields.Str(required=True)
