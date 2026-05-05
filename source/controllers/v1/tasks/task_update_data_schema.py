from marshmallow import fields, post_load

from source.controllers.v1.tasks.task_entity import TaskUpdateDataEntity
from source.controllers.v1.tasks.task_data_schema import TaskDataSchema
from source.models.task import TaskStatus


class TaskUpdateDataSchema(TaskDataSchema):
    status = fields.Enum(TaskStatus, by_value=True, required=True)

    @post_load
    def make_entity(self, data: dict, **kwargs: object) -> TaskUpdateDataEntity:
        return TaskUpdateDataEntity(
            title=data["title"],
            description=data["description"],
            due_date=data["due_date"],
            status=data["status"],
        )
