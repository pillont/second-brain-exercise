from itertools import chain
from typing import Iterable, List, Optional

from source.models.filtered_list import FilteredList, map_to_filtered
from source.models.not_found_error import NotFoundError
from source.models.task import Task, TaskData, TaskStatus, TaskUpdateData
from source.models.task_filters import TaskFilters
from source.models.task_sort import TaskSort
from source.repositories.create_task_repository import CreateTaskRepository
from source.repositories.delete_task_repository import DeleteTaskRepository
from source.repositories.get_all_tasks_repository import GetAllTasksRepository
from source.repositories.get_task_repository import GetTaskRepository
from source.repositories.update_task_repository import UpdateTaskRepository


class FakeTaskRepository(
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
        cursor: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> FilteredList[Task]:
        elements: Iterable[Task] = chain(self._tasks)

        if filters:
            elements = filters.apply(elements)

        sorted_elements: List[Task] = sort.apply(elements) if sort else list(elements)

        if cursor:
            sorted_elements = self._filtered_by_cursor(sorted_elements, cursor)

        return map_to_filtered(sorted_elements, page_size)

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

    def _filtered_by_cursor(self, elements: List[Task], cursor: int) -> List[Task]:
        for i, task in enumerate(elements):
            if task.id == cursor:
                return elements[i + 1 :]
        return elements
