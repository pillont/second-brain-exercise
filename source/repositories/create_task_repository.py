from abc import ABC, abstractmethod

from source.models.task import Task, TaskData


class CreateTaskRepository(ABC):
    @abstractmethod
    def create(self, task_data: TaskData) -> Task: ...
