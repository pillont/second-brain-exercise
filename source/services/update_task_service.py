from typing import Final

from source.models.task import TaskUpdateData
from source.repositories.update_task_repository import UpdateTaskRepository


class UpdateTaskService:
    def __init__(self, repository: UpdateTaskRepository) -> None:
        self._repository: Final = repository

    def update_task(self, id: int, task_update_data: TaskUpdateData) -> None:
        self._repository.update(id, task_update_data)
