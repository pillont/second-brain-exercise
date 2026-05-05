from marshmallow import fields

from source.controllers.v1.schemas.list_argument_schema import \
    ListArgumentSchema
from source.models.task import TaskStatus
from source.models.task_sort import SortDirection, SortField


class TasksListArgumentSchema(ListArgumentSchema):
    status = fields.Enum(TaskStatus, by_value=True, required=False)
    due_date_from = fields.Date(required=False)
    due_date_to = fields.Date(required=False)
    title = fields.String(required=False)
    sort_by = fields.Enum(SortField, by_value=True, required=False)
    sort_direction = fields.Enum(SortDirection, by_value=True, required=False)
