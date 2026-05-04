from datetime import date
from itertools import chain
from typing import Iterable, List, Optional, Union

from source.models.filtered_list import FilteredList, map_to_filtered_list
from source.models.not_found_error import NotFoundError
from source.models.task import Task, TaskData, TaskStatus, TaskUpdateData
from source.models.task_cursor import (
    TaskCursor,
    convert_cursor_sort_value,
    encode_task_cursor,
)
from source.models.task_filters import TaskFilters
from source.models.task_sort import SortDirection, SortField, TaskSort
from source.repositories.create_task_repository import CreateTaskRepository
from source.repositories.delete_task_repository import DeleteTaskRepository
from source.repositories.fake.tasks_list_filter import filter_tasks_list
from source.repositories.get_all_tasks_repository import GetAllTasksRepository
from source.repositories.get_task_repository import GetTaskRepository
from source.repositories.update_task_repository import UpdateTaskRepository


def _get_task_sort_value(
    task: Task, field: SortField
) -> Union[str, int, date, TaskStatus]:
    match field:
        case SortField.TITLE:
            return task.title.lower()
        case SortField.DUE_DATE:
            return task.due_date
        case SortField.STATUS:
            return task.status
        case _:
            return task.id


def _is_after_cursor(
    task: Task,
    field: SortField,
    prev_value: Union[str, int, date, TaskStatus],
    prev_id: int,
    asc: bool,
) -> bool:
    val = _get_task_sort_value(task, field)
    if field == SortField.ID:
        return val > prev_id if asc else val < prev_id  # type: ignore[operator]
    if asc:
        return val > prev_value or (val == prev_value and task.id > prev_id)  # type: ignore[operator]
    return val < prev_value or (val == prev_value and task.id > prev_id)  # type: ignore[operator]


def _filter_by_cursor(
    elements: List[Task], cursor: TaskCursor, sort: Optional[TaskSort]
) -> List[Task]:
    field = sort.field if sort else SortField.ID
    asc = (sort.direction if sort else SortDirection.ASC) == SortDirection.ASC
    prev = convert_cursor_sort_value(cursor.sort_value, field)
    return [t for t in elements if _is_after_cursor(t, field, prev, cursor.id, asc)]


def _compute_next_cursor(
    tasks: List[Task], page_size: int, sort: Optional[TaskSort]
) -> Optional[str]:
    if len(tasks) < page_size:
        return None
    last_task = tasks[page_size - 1]
    return encode_task_cursor(last_task, sort or TaskSort())


class TasksFakeRepository(
    CreateTaskRepository,
    GetAllTasksRepository,
    GetTaskRepository,
    UpdateTaskRepository,
    DeleteTaskRepository,
):
    def __init__(self) -> None:
        self._tasks: List[Task] = []
        self._next_id: int = 1

    def create(self, task_data: TaskData) -> Task:
        task = self._to_task(task_data)
        self._tasks.append(task)
        self._next_id += 1
        return task

    def get_all(
        self,
        filters: Optional[TaskFilters] = None,
        sort: Optional[TaskSort] = None,
        cursor: Optional[TaskCursor] = None,
        page_size: Optional[int] = None,
    ) -> FilteredList[Task]:
        elements: Iterable[Task] = chain(self._tasks)

        if filters:
            elements = filter_tasks_list(self._tasks, filters)

        sorted_elements: List[Task] = sort.apply(elements) if sort else list(elements)

        if cursor:
            sorted_elements = _filter_by_cursor(sorted_elements, cursor, sort)

        filtered = map_to_filtered_list(sorted_elements, page_size)
        next_cursor = (
            _compute_next_cursor(sorted_elements, page_size, sort)
            if page_size and filtered.has_next
            else None
        )
        return FilteredList(filtered.elements, filtered.has_next, next_cursor)

    def get_task(self, id: int) -> Task:
        return self._find_by_id(id)

    def update(self, id: int, task_update_data: TaskUpdateData) -> None:
        task = self._find_by_id(id)
        self.update_task(task, task_update_data)

    def update_task(self, task: Task, task_update_data: TaskUpdateData) -> None:
        task.title = task_update_data.title
        task.description = task_update_data.description
        task.due_date = task_update_data.due_date
        task.status = task_update_data.status

    def delete_task(self, id: int) -> None:
        value = self._find_by_id(id)
        self._tasks.remove(value)

    def _to_task(self, task_data: TaskData) -> Task:
        return Task(
            id=self._next_id,
            title=task_data.title,
            description=task_data.description,
            due_date=task_data.due_date,
            status=TaskStatus.INCOMPLETE,
        )

    def _find_by_id(self, id: int) -> Task:
        try:
            return next(task for task in self._tasks if task.id == id)
        except StopIteration:
            raise NotFoundError()
