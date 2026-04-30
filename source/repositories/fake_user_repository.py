from typing import List

from source.models.not_found_error import NotFoundError
from source.models.user import HashedUserData, User
from source.models.user_already_exists_error import UserAlreadyExistsError
from source.repositories.get_user_by_username_repository import (
    GetUserByUsernameRepository,
)
from source.repositories.register_user_repository import RegisterUserRepository


class FakeUserRepository(RegisterUserRepository, GetUserByUsernameRepository):
    def __init__(self) -> None:
        self._users: List[User] = []
        self._next_id: int = 1

    def register(self, user_data: HashedUserData) -> User:
        if self._username_exists(user_data.username):
            raise UserAlreadyExistsError()
        user = self._to_user(user_data)
        self._users.append(user)
        self._next_id += 1
        return user

    def get_by_username(self, username: str) -> User:
        try:
            return next(u for u in self._users if u.username == username)
        except StopIteration:
            raise NotFoundError()

    def _to_user(self, user_data: HashedUserData) -> User:
        return User(
            id=self._next_id,
            username=user_data.username,
            hashed_password=user_data.hashed_password,
        )

    def _username_exists(self, username: str) -> bool:
        return any(u.username == username for u in self._users)
