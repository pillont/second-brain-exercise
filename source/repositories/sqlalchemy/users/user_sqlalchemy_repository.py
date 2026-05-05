from typing import Final

from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from source.models.not_found_error import NotFoundError
from source.models.user import HashedUserData, User
from source.repositories.get_user_by_username_repository import GetUserByUsernameRepository
from source.repositories.register_user_repository import RegisterUserRepository
from source.repositories.sqlalchemy.session_utils import (OrmSession, initialize_schema)
from source.repositories.sqlalchemy.users.user_orm_model import UserOrmModel


class UsersSqlalchemyRepository(GetUserByUsernameRepository, RegisterUserRepository):
    def __init__(self, engine: Engine) -> None:
        self._orm_session: Final = OrmSession(initialize_schema(engine), UserOrmModel)

    def get_by_username(self, username: str) -> User:
        with Session(self._orm_session.engine) as session:
            user_orm = session\
                .query(UserOrmModel)\
                .filter_by(username=username)\
                .first()
            
        if not user_orm:
            raise NotFoundError()
        
        return User(id=user_orm.id, username=user_orm.username, hashed_password=user_orm.hashed_password)
        
    def register(self, user_data: HashedUserData) -> User:
            user_orm = UserOrmModel(username=user_data.username, hashed_password=user_data.hashed_password)

            self._orm_session.add(user_orm)

            return User(id=user_orm.id, username=user_orm.username, hashed_password=user_orm.hashed_password)

