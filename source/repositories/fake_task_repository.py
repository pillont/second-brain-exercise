from typing import Iterable, List

from source.models.not_found_error import NotFoundError
from source.models.task import Task, TaskData, TaskStatus, TaskUpdateData
from source.repositories.create_task_repository import CreateTaskRepository
from source.repositories.get_all_tasks_repository import GetAllTasksRepository
from source.repositories.get_task_repository import GetTaskRepository
from source.repositories.update_task_repository import UpdateTaskRepository


class FakeTaskRepository(
    CreateTaskRepository,
    GetAllTasksRepository,
    GetTaskRepository,
    UpdateTaskRepository,
):
    def __init__(self) -> None:
        self._tasks: List[Task] = []
        self._next_id: int = 1

    def create(self, task_data: TaskData) -> Task:
        task = self._to_task(task_data)
        self._tasks.append(task)
        self._next_id += 1
        return task

    def get_all(self) -> Iterable[Task]:
        return (t for t in self._tasks)

    def get_task(self, id: int) -> Task:
        return self._find_by_id(id)

    def update(self, id: int, task_update_data: TaskUpdateData) -> None:
        task = self._find_by_id(id)
        self.update_task(task, task_update_data)

    def update_task(self, task: Task, task_update_data: TaskUpdateData)-> None:
        task.title = task_update_data.title
        task.description = task_update_data.description
        task.due_date = task_update_data.due_date
        task.status = task_update_data.status

    def _to_task(self, task_data: TaskData) -> Task:
        return Task(
            id=self._next_id,
            title=task_data.title,
            description=task_data.description,
            due_date=task_data.due_date,
            status=TaskStatus.INCOMPLETE,
        )

    def _find_by_id(self, id: int) -> Task:
        try:
            return next(task for task in self._tasks if task.id == id)
        except StopIteration:
            raise NotFoundError()
