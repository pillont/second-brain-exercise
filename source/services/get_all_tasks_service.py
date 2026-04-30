from typing import Final, Generator

from source.models.task import Task
from source.repositories.get_all_tasks_repository import GetAllTasksRepository


class GetAllTasksService:
    def __init__(self, repository: GetAllTasksRepository) -> None:
        self._repository: Final = repository

    def get_all_tasks(self) -> Generator[Task]:
        return self._repository.get_all()
