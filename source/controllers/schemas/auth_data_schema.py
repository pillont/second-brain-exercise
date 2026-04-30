from marshmallow import Schema, fields


class AuthDataSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
