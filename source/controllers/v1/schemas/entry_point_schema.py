from marshmallow import Schema, fields

from source.controllers.v1.schemas.link_schema import LinkSchema, LinksSchema


class EntryPointLinksSchema(LinksSchema):
    register = fields.Nested(LinkSchema)
    login = fields.Nested(LinkSchema)


class EntryPointSchema(Schema):
    links = fields.Nested(EntryPointLinksSchema, data_key="_links", required=True)
