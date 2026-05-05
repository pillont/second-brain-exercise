from typing import Final

from werkzeug.security import check_password_hash

from source.config.app_config import AppConfig
from source.models.invalid_credentials_error import InvalidCredentialsError
from source.models.not_found_error import NotFoundError
from source.models.user import User
from source.repositories.get_user_by_username_repository import \
    GetUserByUsernameRepository


class LoginUserService:
    def __init__(
        self, repository: GetUserByUsernameRepository, config: AppConfig
    ) -> None:
        self._repository: Final = repository
        self._config: Final = config

    def login(self, username: str, password: str) -> User:
        user = self._get_user(username)
        self._validate_password_or_throw(user, password)
        return user

    def _validate_password_or_throw(self, user: User, password: str) -> None:
        if not check_password_hash(user.hashed_password, password):
            raise InvalidCredentialsError()

    def _get_user(self, username: str) -> User:
        try:
            return self._repository.get_by_username(username)
        except NotFoundError:
            raise InvalidCredentialsError()
