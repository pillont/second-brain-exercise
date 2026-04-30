from marshmallow import Schema, fields
from source.controllers.schemas.link_schema import LinksSchema


class TaskSchema(Schema):
    id = fields.Int(required=True)
    title = fields.Str(required=True)
    description = fields.Str(required=True)
    due_date = fields.Date(required=True)
    status = fields.Str(required=True)
    links = fields.Nested(LinksSchema, data_key="_links", required=True)
