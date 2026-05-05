from marshmallow import Schema, fields, post_load

from source.controllers.v1.tasks.task_entity import TaskDataEntity


class TaskDataSchema(Schema):
    title = fields.Str(required=True)
    description = fields.Str(required=True)
    due_date = fields.Date(required=True)

    @post_load
    def make_entity(self, data: dict, **kwargs: object) -> TaskDataEntity:
        return TaskDataEntity(
            title=data["title"],
            description=data["description"],
            due_date=data["due_date"],
        )
