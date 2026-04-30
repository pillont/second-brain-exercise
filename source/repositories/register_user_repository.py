from abc import ABC, abstractmethod
from source.models.user import User, UserData


class RegisterUserRepository(ABC):
    @abstractmethod
    def register(self, user_data: UserData) -> User: ...
