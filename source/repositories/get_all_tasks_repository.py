from abc import ABC, abstractmethod
from typing import Optional

from source.models.filtered_list import FilteredList
from source.models.task import Task
from source.models.task_filters import TaskFilters
from source.models.task_sort import TaskSort


class GetAllTasksRepository(ABC):
    @abstractmethod
    def get_all(
        self,
        filters: Optional[TaskFilters] = None,
        sort: Optional[TaskSort] = None,
        cursor: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> FilteredList[Task]: ...
