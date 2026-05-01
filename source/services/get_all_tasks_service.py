from typing import Final, Optional

from source.models.filtered_list import FilteredList
from source.models.task import Task
from source.models.task_filters import TaskFilters
from source.repositories.get_all_tasks_repository import GetAllTasksRepository


class GetAllTasksService:
    def __init__(self, repository: GetAllTasksRepository) -> None:
        self._repository: Final = repository

    def get_all_tasks(
        self,
        filters: Optional[TaskFilters] = None,
        cursor: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> FilteredList[Task]:
        return self._repository.get_all(filters, cursor, page_size)
