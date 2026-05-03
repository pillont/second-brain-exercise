from marshmallow import Schema, fields

from source.controllers.schemas.link_schema import LinkSchema, LinksSchema


class TokenLinksSchema(LinksSchema):
    register = fields.Nested(LinkSchema, required=True)
    get_all_tasks = fields.Nested(LinkSchema, required=True)
    create_task = fields.Nested(LinkSchema, required=True)


class TokenSchema(Schema):
    token = fields.Str(required=True)
    links = fields.Nested(TokenLinksSchema, data_key="_links", required=True)
