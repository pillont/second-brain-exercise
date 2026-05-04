from marshmallow import Schema, fields
from source.controllers.schemas.link_schema import LinkSchema, LinksSchema
from source.models.task import TaskStatus


class TaskLinksSchema(LinksSchema):
    tasks = fields.Nested(LinkSchema, required=True)
    update = fields.Nested(LinkSchema, required=True)
    delete = fields.Nested(LinkSchema, required=True)


class TaskSchema(Schema):
    id = fields.Int(required=True)
    title = fields.Str(required=True)
    description = fields.Str(required=True)
    due_date = fields.Date(required=True)
    status = fields.Enum(TaskStatus, by_value=True, required=True)
    links = fields.Nested(TaskLinksSchema, data_key="_links", required=True)


class TasksListSchema(Schema):
    elements = fields.List(fields.Nested(TaskSchema))
    has_next = fields.Bool(required=True)
    next_cursor = fields.Str(allow_none=True, load_default=None)
