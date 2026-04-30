from typing import Iterable

from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint
from dependency_injector.wiring import inject, Provide
from source.container import Container
from source.controllers.entities.task_entity import (
    TaskDataEntity,
    TaskEntity,
    TaskUpdateDataEntity,
)
from source.controllers.mappers.task_mapper import (
    to_task_data,
    to_task_entity,
    to_task_update_data,
)
from source.controllers.schemas.task_data_schema import TaskDataSchema
from source.controllers.schemas.task_schema import TaskSchema
from source.controllers.schemas.task_update_data_schema import TaskUpdateDataSchema
from source.services.create_task_service import CreateTaskService
from source.services.delete_task_service import DeleteTaskService
from source.services.get_all_tasks_service import GetAllTasksService
from source.services.get_task_service import GetTaskService
from source.services.update_task_service import UpdateTaskService

tasks_blp = Blueprint("tasks", __name__, url_prefix="/tasks")


@tasks_blp.route("/", methods=["POST"])
@jwt_required()
@tasks_blp.arguments(TaskDataSchema)
@tasks_blp.response(201, TaskSchema)
@inject
def create_task(
    task_data_entity: TaskDataEntity,
    create_task_service: CreateTaskService = Provide[Container.create_task_service],
) -> TaskEntity:
    task = create_task_service.create_task(to_task_data(task_data_entity))
    return to_task_entity(task)


@tasks_blp.route("/", methods=["GET"])
@jwt_required()
@tasks_blp.response(200, TaskSchema(many=True))
@inject
def get_all_tasks(
    get_all_tasks_service: GetAllTasksService = Provide[
        Container.get_all_tasks_service
    ],
) -> Iterable[TaskEntity]:
    all_tasks = get_all_tasks_service.get_all_tasks()
    return (to_task_entity(task) for task in all_tasks)


@tasks_blp.route("/<int:id>", methods=["GET"])
@jwt_required()
@tasks_blp.response(404)
@tasks_blp.response(200, TaskSchema)
@inject
def get_task(
    id: int,
    get_task_service: GetTaskService = Provide[Container.get_task_service],
) -> TaskEntity:
    task = get_task_service.get_task(id)
    return to_task_entity(task)


@tasks_blp.route("/<int:id>", methods=["PUT"])
@jwt_required()
@tasks_blp.arguments(TaskUpdateDataSchema)
@tasks_blp.response(404)
@tasks_blp.response(204)
@inject
def update_task(
    task_update_data_entity: TaskUpdateDataEntity,
    id: int,
    update_task_service: UpdateTaskService = Provide[Container.update_task_service],
) -> None:
    update_task_service.update_task(id, to_task_update_data(task_update_data_entity))


@tasks_blp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
@tasks_blp.response(404)
@tasks_blp.response(204)
@inject
def delete_task(
    id: int,
    delete_task_service: DeleteTaskService = Provide[Container.delete_task_service],
) -> None:
    delete_task_service.delete_task(id)
