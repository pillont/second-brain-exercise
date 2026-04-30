from abc import ABC, abstractmethod


class DeleteTaskRepository(ABC):
    @abstractmethod
    def delete_task(self, id: int) -> None: ...
