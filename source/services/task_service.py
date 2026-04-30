from source.models.task import Task, TaskData
from source.repositories.create_task_repository import CreateTaskRepository


class CreateTaskService:
    def __init__(self, repository: CreateTaskRepository) -> None:
        self._repository = repository

    def create_task(self, task_data: TaskData) -> Task:
        return self._repository.create(task_data)
