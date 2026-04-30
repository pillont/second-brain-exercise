from typing import Any, Dict

from marshmallow import fields, post_load

from source.controllers.entities.task_entity import TaskUpdateDataEntity
from source.controllers.schemas.task_data_schema import TaskDataSchema


class TaskUpdateDataSchema(TaskDataSchema):
    status = fields.Str(required=True)

    @post_load
    def make_entity(self, data: dict, **kwargs: object) -> TaskUpdateDataEntity:
        return TaskUpdateDataEntity(
            title=data["title"],
            description=data["description"],
            due_date=data["due_date"],
            status=data["status"],
        )
