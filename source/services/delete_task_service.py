from typing import Final

from source.models.task import TaskUpdateData
from source.repositories.delete_task_repository import DeleteTaskRepository


class DeleteTaskService:
    def __init__(self, repository: DeleteTaskRepository) -> None:
        self._repository: Final = repository

    def delete_task(self, id: int) -> None:
        self._repository.delete_task(id)
