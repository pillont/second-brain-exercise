from marshmallow import fields

from source.controllers.schemas.list_argument_schema import ListArgumentSchema
from source.models.task import TaskStatus


class TasksListArgumentSchema(ListArgumentSchema):
    status = fields.Enum(TaskStatus, by_value=True, required=False)
    due_date_from = fields.Date(required=False)
    due_date_to = fields.Date(required=False)
    title = fields.String(required=False)
    description = fields.String(required=False)
