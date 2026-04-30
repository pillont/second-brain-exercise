from typing import Iterable

from flask_smorest import Blueprint
from dependency_injector.wiring import inject, Provide
from source.container import Container
from source.controllers.entities.task_entity import TaskDataEntity, TaskEntity
from source.controllers.mappers.task_mapper import to_task_data, to_task_entity
from source.controllers.schemas.task_data_schema import TaskDataSchema
from source.controllers.schemas.task_schema import TaskSchema
from source.services.create_task_service import CreateTaskService
from source.services.get_all_tasks_service import GetAllTasksService
from source.services.get_task_service import GetTaskService

tasks_blp = Blueprint("tasks", __name__, url_prefix="/tasks")


@tasks_blp.route("/", methods=["POST"])
@tasks_blp.arguments(TaskDataSchema)
@tasks_blp.response(201, TaskSchema)
@inject
def create_task(
    task_data_entity: TaskDataEntity,
    create_task_service: CreateTaskService=Provide[Container.create_task_service],
) -> TaskEntity:
    task = create_task_service.create_task(to_task_data(task_data_entity))
    return to_task_entity(task)


@tasks_blp.route("/", methods=["GET"])
@tasks_blp.response(200, TaskSchema(many=True))
@inject
def get_all_tasks(
    get_all_tasks_service: GetAllTasksService=Provide[Container.get_all_tasks_service],
) -> Iterable[TaskEntity]:
    all_tasks = get_all_tasks_service.get_all_tasks()
    return (to_task_entity(task) for task in all_tasks)

@tasks_blp.route("/<int:id>", methods=["GET"])
@tasks_blp.response(404, None)
@tasks_blp.response(200, TaskSchema)
@inject
def get_task(
    id:int,
    get_task_service: GetTaskService =Provide[Container.get_task_service],
) -> TaskEntity:
    task = get_task_service.get_task(id)
    return to_task_entity(task)
