from typing import Final

from sqlalchemy.engine import Engine

from source.models.task import Task, TaskData
from source.repositories.create_task_repository import CreateTaskRepository
from source.repositories.sqlalchemy.session_utils import OrmSession, initialize_schema
from source.repositories.sqlalchemy.tasks.repositories.create.task_sqlalchemy_mapper import (
    to_orm_task,
    to_task,
)
from source.repositories.sqlalchemy.tasks.task_orm_model import TaskOrmModel


class CreateTaskSqlalchemyRepository(CreateTaskRepository):
    def __init__(self, engine: Engine) -> None:
        self._orm_session: Final = OrmSession(initialize_schema(engine), TaskOrmModel)

    def create(self, task_data: TaskData) -> Task:
        orm_task = to_orm_task(task_data)
        self._orm_session.add(orm_task)
        return to_task(orm_task)
