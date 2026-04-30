from abc import ABC, abstractmethod
from source.models.task import Task


class GetTaskRepository(ABC):
    @abstractmethod
    def get_task(self, id: int) -> Task: ...
