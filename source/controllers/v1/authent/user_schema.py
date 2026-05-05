from marshmallow import Schema, fields

from source.controllers.v1.utils.link_schema import LinkSchema, LinksSchema


class UserLinksSchema(LinksSchema):
    login = fields.Nested(LinkSchema, required=True)


class UserSchema(Schema):
    id = fields.Int(required=True)
    username = fields.Str(required=True)
    links = fields.Nested(UserLinksSchema, data_key="_links", required=True)
