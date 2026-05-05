from marshmallow import Schema, fields, post_load

from source.controllers.v1.tasks.task_dto import TaskDataDTO


class TaskDataSchema(Schema):
    title = fields.Str(required=True)
    description = fields.Str(required=True)
    due_date = fields.Date(required=True)

    @post_load
    def make_dto(self, data: dict, **kwargs: object) -> TaskDataDTO:
        return TaskDataDTO(
            title=data["title"],
            description=data["description"],
            due_date=data["due_date"],
        )
