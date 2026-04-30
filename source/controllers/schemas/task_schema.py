from marshmallow import Schema, fields
from source.controllers.schemas.link_schema import LinkSchema, LinksSchema


class TaskLinksSchema(LinksSchema):
    tasks = fields.Nested(LinkSchema, required=True)
    update = fields.Nested(LinkSchema, required=True)


class TaskSchema(Schema):
    id = fields.Int(required=True)
    title = fields.Str(required=True)
    description = fields.Str(required=True)
    due_date = fields.Date(required=True)
    status = fields.Str(required=True)
    links = fields.Nested(TaskLinksSchema, data_key="_links", required=True)
