from typing import Final

from sqlalchemy.engine import Engine

from source.repositories.delete_task_repository import DeleteTaskRepository
from source.repositories.sqlalchemy.session_utils import (OrmSession,
                                                          initialize_schema)
from source.repositories.sqlalchemy.tasks.task_orm_model import TaskOrmModel


class DeleteTaskSqlalchemyRepository(DeleteTaskRepository):
    def __init__(self, engine: Engine) -> None:
        self._orm_session: Final = OrmSession(initialize_schema(engine), TaskOrmModel)

    def delete_task(self, id: int) -> None:
        self._orm_session.delete_or_raise(id)
