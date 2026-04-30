from abc import ABC, abstractmethod
from typing import Iterable, Optional
from source.models.task import Task


class GetAllTasksRepository(ABC):
    @abstractmethod
    def get_all(self, cursor: Optional[int] =None, page_size: Optional[int]=None) -> Iterable[Task]: ...
