from abc import ABC, abstractmethod
from typing import Optional

from source.models.filtered_list import FilteredList
from source.models.task import Task
from source.models.task_filters import TaskFilters


class GetAllTasksRepository(ABC):
    @abstractmethod
    def get_all(
        self,
        filters: Optional[TaskFilters] = None,
        cursor: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> FilteredList[Task]: ...
