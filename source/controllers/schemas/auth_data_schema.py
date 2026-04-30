from marshmallow import Schema, fields, validate


class AuthDataSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(
        required=True, load_only=True, validate=validate.Length(min=8)
    )
