from typing import Final

from werkzeug.security import generate_password_hash

from source.models.user import User, UserData
from source.repositories.register_user_repository import RegisterUserRepository


class RegisterUserService:
    def __init__(self, repository: RegisterUserRepository) -> None:
        self._repository: Final = repository

    def register_user(self, user_data: UserData) -> User:
        hashed = UserData(
            username=user_data.username,
            password=generate_password_hash(user_data.password),
        )
        return self._repository.register(hashed)
