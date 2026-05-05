from typing import Final

from sqlalchemy.engine import Engine

from source.models.task import TaskUpdateData
from source.repositories.sqlalchemy.session_utils import (OrmSession,
                                                          initialize_schema)
from source.repositories.sqlalchemy.tasks.task_orm_model import TaskOrmModel
from source.repositories.update_task_repository import UpdateTaskRepository


def _apply_update(orm_task: TaskOrmModel, task_update_data: TaskUpdateData) -> None:
    orm_task.title = task_update_data.title
    orm_task.description = task_update_data.description
    orm_task.due_date = task_update_data.due_date
    orm_task.status = str(task_update_data.status)


class UpdateTaskSqlalchemyRepository(UpdateTaskRepository):
    def __init__(self, engine: Engine) -> None:
        self._orm_session: Final = OrmSession(initialize_schema(engine), TaskOrmModel)

    def update(self, id: int, task_update_data: TaskUpdateData) -> None:
        self._orm_session.update_or_raise(
            id, lambda orm_task: _apply_update(orm_task, task_update_data)
        )
