from abc import ABC, abstractmethod

from source.models.user import User


class GetUserByUsernameRepository(ABC):
    @abstractmethod
    def get_by_username(self, username: str) -> User: ...
