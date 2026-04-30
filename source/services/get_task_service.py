from typing import Final

from source.models.task import Task
from source.repositories.get_task_repository import GetTaskRepository


class GetTaskService:
    def __init__(self, repository: GetTaskRepository) -> None:
        self._repository: Final = repository

    def get_task(self, id: int) -> Task:
        return self._repository.get_task(id)
