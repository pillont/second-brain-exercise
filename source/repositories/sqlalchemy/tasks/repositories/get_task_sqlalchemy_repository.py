from typing import Final

from sqlalchemy.engine import Engine

from source.models.task import Task
from source.repositories.get_task_repository import GetTaskRepository
from source.repositories.sqlalchemy\
    .session_utils import OrmSession, initialize_schema
from source.repositories.sqlalchemy.tasks.task_orm_model import TaskOrmModel
from source.repositories.sqlalchemy.tasks.repositories\
    .create.task_sqlalchemy_mapper import (
        to_task,
    )


class GetTaskSqlalchemyRepository(GetTaskRepository):
    def __init__(self, engine: Engine) -> None:
        self._orm_session: Final = OrmSession(initialize_schema(engine), TaskOrmModel)

    def get_task(self, id: int) -> Task:
        data = self._orm_session.get_or_raise(id)
        return to_task(data)
