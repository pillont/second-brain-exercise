from marshmallow import Schema, fields
from source.controllers.v1.schemas.link_schema import LinksSchema


class GreetingSchema(Schema):
    id = fields.Int(required=True)
    message = fields.Str(required=True)
    links = fields.Nested(LinksSchema, data_key="_links", required=True)
