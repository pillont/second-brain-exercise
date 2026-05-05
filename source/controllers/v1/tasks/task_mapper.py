from typing import Optional

from source.controllers.v1.utils.link import HttpMethod, LinkDTO
from source.controllers.v1.utils.list_dto import ListDTO
from source.controllers.v1.tasks.task_dto import (
    TaskDataDTO,
    TaskDTO,
    TaskLinksDTO,
    TaskUpdateDataDTO,
)
from source.controllers.v1.tasks.tasks_list_argument_dto import (
    TasksListArgumentDTO,
)
from source.controllers.v1.utils.list_dto_mapper import map_to_list_dto
from source.models.filtered_list import FilteredList
from source.models.task import Task, TaskData, TaskUpdateData
from source.models.task_cursor import TaskCursor, decode_task_cursor
from source.models.task_filters import TaskFilters
from source.models.task_sort import SortDirection, SortField, TaskSort


def to_task_filters(DTO: TasksListArgumentDTO) -> TaskFilters:
    return TaskFilters(
        status=DTO.get("status"),
        due_date_from=DTO.get("due_date_from"),
        due_date_to=DTO.get("due_date_to"),
        title=DTO.get("title"),
    )


def to_task_sort(DTO: TasksListArgumentDTO) -> TaskSort:
    return TaskSort(
        field=DTO.get("sort_by") or SortField.ID,
        direction=DTO.get("sort_direction") or SortDirection.ASC,
    )


def to_task_cursor(DTO: TasksListArgumentDTO) -> Optional[TaskCursor]:
    cursor_b64 = DTO.get("cursor")
    return decode_task_cursor(cursor_b64) if cursor_b64 else None


def to_task_data(DTO: TaskDataDTO) -> TaskData:
    return TaskData(
        title=DTO["title"],
        description=DTO["description"],
        due_date=DTO["due_date"],
    )


def to_task_update_data(DTO: TaskUpdateDataDTO) -> TaskUpdateData:
    return TaskUpdateData(
        title=DTO["title"],
        description=DTO["description"],
        due_date=DTO["due_date"],
        status=DTO["status"],
    )


def to_task_dto(task: Task) -> TaskDTO:
    links = _build_links(task)
    return TaskDTO(
        id=task.id,
        title=task.title,
        description=task.description,
        due_date=task.due_date,
        status=task.status,
        links=links,
    )


def map_to_filtered_tasks_list(all_tasks: FilteredList[Task]) -> ListDTO[TaskDTO]:
    return map_to_list_dto(
        FilteredList(
            (to_task_dto(t) for t in all_tasks.elements),
            has_next=all_tasks.has_next,
            next_cursor=all_tasks.next_cursor,
        )
    )


def _build_links(task: Task) -> TaskLinksDTO:
    return TaskLinksDTO(
        self_link=LinkDTO(href=f"/v1/tasks/{task.id}"),
        tasks=LinkDTO(href="/v1/tasks/"),
        update=LinkDTO(href=f"/v1/tasks/{task.id}", type=HttpMethod.PUT),
        delete=LinkDTO(href=f"/v1/tasks/{task.id}", type=HttpMethod.DELETE),
    )
