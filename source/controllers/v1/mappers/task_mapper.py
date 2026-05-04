from typing import Optional

from source.controllers.v1.entities.list_entity import ListEntity
from source.controllers.v1.entities.tasks_list_argument_entity import (
    TasksListArgumentEntity,
)
from source.controllers.v1.mappers.list_entity_mapper import map_to_list_entity
from source.models.filtered_list import FilteredList
from source.models.task import Task, TaskData, TaskUpdateData
from source.models.task_cursor import TaskCursor, decode_task_cursor
from source.models.task_filters import TaskFilters
from source.models.task_sort import SortDirection, SortField, TaskSort
from source.controllers.v1.entities.task_entity import (
    TaskDataEntity,
    TaskEntity,
    TaskLinks,
    TaskUpdateDataEntity,
)
from source.controllers.v1.entities.link import HttpMethod, LinkEntity


def to_task_filters(entity: TasksListArgumentEntity) -> TaskFilters:
    return TaskFilters(
        status=entity.get("status"),
        due_date_from=entity.get("due_date_from"),
        due_date_to=entity.get("due_date_to"),
        title=entity.get("title"),
    )


def to_task_sort(entity: TasksListArgumentEntity) -> TaskSort:
    return TaskSort(
        field=entity.get("sort_by") or SortField.ID,
        direction=entity.get("sort_direction") or SortDirection.ASC,
    )


def to_task_cursor(entity: TasksListArgumentEntity) -> Optional[TaskCursor]:
    cursor_b64 = entity.get("cursor")
    return decode_task_cursor(cursor_b64) if cursor_b64 else None


def to_task_data(entity: TaskDataEntity) -> TaskData:
    return TaskData(
        title=entity["title"],
        description=entity["description"],
        due_date=entity["due_date"],
    )


def to_task_update_data(entity: TaskUpdateDataEntity) -> TaskUpdateData:
    return TaskUpdateData(
        title=entity["title"],
        description=entity["description"],
        due_date=entity["due_date"],
        status=entity["status"],
    )


def to_task_entity(task: Task) -> TaskEntity:
    links = _build_links(task)
    return TaskEntity(
        id=task.id,
        title=task.title,
        description=task.description,
        due_date=task.due_date,
        status=task.status,
        links=links,
    )


def map_to_filtered_tasks_list(all_tasks: FilteredList[Task]) -> ListEntity[TaskEntity]:
    return map_to_list_entity(
        FilteredList(
            (to_task_entity(t) for t in all_tasks.elements),
            has_next=all_tasks.has_next,
            next_cursor=all_tasks.next_cursor,
        )
    )


def _build_links(task: Task) -> TaskLinks:
    return TaskLinks(
        self_link=LinkEntity(href=f"/v1/tasks/{task.id}"),
        tasks=LinkEntity(href="/v1/tasks/"),
        update=LinkEntity(href=f"/v1/tasks/{task.id}", type=HttpMethod.PUT),
        delete=LinkEntity(href=f"/v1/tasks/{task.id}", type=HttpMethod.DELETE),
    )
