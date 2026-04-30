from abc import ABC, abstractmethod

from source.models.task import TaskUpdateData


class UpdateTaskRepository(ABC):
    @abstractmethod
    def update(self, id: int, task_update_data: TaskUpdateData) -> None: ...
