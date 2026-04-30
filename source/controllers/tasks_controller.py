from typing import Iterable

from flask_smorest import Blueprint
from dependency_injector.wiring import inject, Provide
from source.container import Container
from source.controllers.entities.task_entity import TaskDataEntity, TaskEntity
from source.controllers.mappers.task_mapper import to_task_data, to_task_entity
from source.controllers.schemas.task_data_schema import TaskDataSchema
from source.controllers.schemas.task_schema import TaskSchema

tasks_blp = Blueprint("tasks", __name__, url_prefix="/tasks")


@tasks_blp.route("/", methods=["POST"])
@tasks_blp.arguments(TaskDataSchema)
@tasks_blp.response(201, TaskSchema)
@inject
def create_task(
    task_data_entity: TaskDataEntity,
    create_task_service=Provide[Container.create_task_service],
) -> TaskEntity:
    task = create_task_service.create_task(to_task_data(task_data_entity))
    return to_task_entity(task)


@tasks_blp.route("/", methods=["GET"])
@tasks_blp.response(200, TaskSchema(many=True))
@inject
def get_tasks(
    get_all_tasks_service=Provide[Container.get_all_tasks_service],
) -> Iterable[TaskEntity]:
    all_tasks = get_all_tasks_service.get_all_tasks()
    return (to_task_entity(task) for task in all_tasks)
