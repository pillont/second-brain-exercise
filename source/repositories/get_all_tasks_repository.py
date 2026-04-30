from abc import ABC, abstractmethod
from typing import Generator
from source.models.task import Task


class GetAllTasksRepository(ABC):
    @abstractmethod
    def get_all(self) -> Generator[Task]: ...
