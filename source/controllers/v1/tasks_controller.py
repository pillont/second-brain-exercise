from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint
from dependency_injector.wiring import inject, Provide
from source.container import Container
from source.controllers.v1.entities.tasks_list_argument_entity import (
    TasksListArgumentEntity,
)
from source.controllers.v1.entities.list_entity import ListEntity
from source.controllers.v1.entities.task_entity import (
    TaskDataEntity,
    TaskEntity,
    TaskUpdateDataEntity,
)
from source.controllers.v1.mappers.task_mapper import (
    map_to_filtered_tasks_list,
    to_task_cursor,
    to_task_data,
    to_task_entity,
    to_task_filters,
    to_task_sort,
    to_task_update_data,
)
from source.controllers.v1.schemas.tasks_list_argument_schema import (
    TasksListArgumentSchema,
)
from source.controllers.v1.schemas.task_data_schema import TaskDataSchema
from source.controllers.v1.schemas.task_schema import TasksListSchema, TaskSchema
from source.controllers.v1.schemas.task_update_data_schema import TaskUpdateDataSchema
from source.services.create_task_service import CreateTaskService
from source.services.delete_task_service import DeleteTaskService
from source.services.get_all_tasks_service import GetAllTasksService
from source.services.get_task_service import GetTaskService
from source.services.update_task_service import UpdateTaskService

v1_tasks_blp = Blueprint(
    "tasks", __name__, url_prefix="/v1/tasks", description="Task management."
)


@v1_tasks_blp.route("/", methods=["POST"])
@jwt_required()
@v1_tasks_blp.doc(summary="Create a task", description="Create a new task.")
@v1_tasks_blp.arguments(TaskDataSchema)
@v1_tasks_blp.response(201, TaskSchema)
@inject
def create_task(
    task_data_entity: TaskDataEntity,
    create_task_service: CreateTaskService = Provide[Container.create_task_service],
) -> TaskEntity:
    task = create_task_service.create_task(to_task_data(task_data_entity))
    return to_task_entity(task)


@v1_tasks_blp.route("/", methods=["GET"])
@jwt_required()
@v1_tasks_blp.doc(
    summary="List tasks",
    description="Retrieve all tasks with optional filters and pagination.",
)
@v1_tasks_blp.arguments(TasksListArgumentSchema, location="query")
@v1_tasks_blp.response(200, TasksListSchema)
@inject
def get_all_tasks(
    args: TasksListArgumentEntity,
    get_all_tasks_service: GetAllTasksService = Provide[
        Container.get_all_tasks_service
    ],
) -> ListEntity[TaskEntity]:
    all_tasks = get_all_tasks_service.get_all_tasks(
        to_task_filters(args),
        to_task_sort(args),
        to_task_cursor(args),
        args.get("page_size", None),
    )

    return map_to_filtered_tasks_list(all_tasks)


@v1_tasks_blp.route("/<int:id>", methods=["GET"])
@jwt_required()
@v1_tasks_blp.doc(summary="Get a task", description="Retrieve a single task by its ID.")
@v1_tasks_blp.response(404)
@v1_tasks_blp.response(200, TaskSchema)
@inject
def get_task(
    id: int,
    get_task_service: GetTaskService = Provide[Container.get_task_service],
) -> TaskEntity:
    task = get_task_service.get_task(id)
    return to_task_entity(task)


@v1_tasks_blp.route("/<int:id>", methods=["PUT"])
@jwt_required()
@v1_tasks_blp.doc(
    summary="Update a task", description="Update an existing task by its ID."
)
@v1_tasks_blp.arguments(TaskUpdateDataSchema)
@v1_tasks_blp.response(404)
@v1_tasks_blp.response(204)
@inject
def update_task(
    task_update_data_entity: TaskUpdateDataEntity,
    id: int,
    update_task_service: UpdateTaskService = Provide[Container.update_task_service],
) -> None:
    update_task_service.update_task(id, to_task_update_data(task_update_data_entity))


@v1_tasks_blp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
@v1_tasks_blp.doc(summary="Delete a task", description="Delete a task by its ID.")
@v1_tasks_blp.response(404)
@v1_tasks_blp.response(204)
@inject
def delete_task(
    id: int,
    delete_task_service: DeleteTaskService = Provide[Container.delete_task_service],
) -> None:
    delete_task_service.delete_task(id)
