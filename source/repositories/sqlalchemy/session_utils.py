from typing import Callable, Final, Generic, List, TypeVar

from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from sqlalchemy.sql import Select

from source.models.not_found_error import NotFoundError
from source.repositories.sqlalchemy.tasks.task_orm_model import Base

T = TypeVar("T")


def initialize_schema(engine: Engine) -> Engine:
    Base.metadata.create_all(engine)
    return engine


class OrmSession(Generic[T]):
    def __init__(self, engine: Engine, model_class: type[T]) -> None:
        self._engine: Final = engine
        self._model_class: Final = model_class

    def add(self, orm_object: Base) -> None:
        with Session(self._engine) as session:
            session.add(orm_object)
            session.commit()
            session.refresh(orm_object)

    def get_or_raise(self, DTO_id: int) -> T:
        with Session(self._engine) as session:
            return self._get_or_raise_in_session(session, DTO_id)

    def select(self, select_statement: Select) -> List[T]:
        with Session(self._engine) as session:
            execusion = session.execute(select_statement).scalars().all()
            return list(execusion)

    def update_or_raise(
        self, DTO_id: int, apply_update: Callable[[T], None]
    ) -> None:
        with Session(self._engine) as session:
            instance = self._get_or_raise_in_session(session, DTO_id)
            apply_update(instance)
            session.commit()

    def delete_or_raise(self, DTO_id: int) -> None:
        with Session(self._engine) as session:
            instance = self._get_or_raise_in_session(session, DTO_id)
            session.delete(instance)
            session.commit()

    def _get_or_raise_in_session(self, session: Session, DTO_id: int) -> T:
        instance = session.get(self._model_class, DTO_id)
        if instance is None:
            raise NotFoundError()
        return instance
