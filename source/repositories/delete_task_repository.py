from abc import ABC, abstractmethod
from source.models.task import Task


class DeleteTaskRepository(ABC):
    @abstractmethod
    def delete_task(self, id: int) -> None: ...
