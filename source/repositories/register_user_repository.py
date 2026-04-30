from abc import ABC, abstractmethod
from source.models.user import HashedUserData, User


class RegisterUserRepository(ABC):
    @abstractmethod
    def register(self, user_data: HashedUserData) -> User: ...
