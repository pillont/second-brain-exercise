import pkgutil
import logging
import source.controllers
from typing import List
from dependency_injector import containers, providers
from source.services.create_task_service import CreateTaskService
from source.services.delete_task_service import DeleteTaskService
from source.services.get_all_tasks_service import GetAllTasksService
from source.services.get_task_service import GetTaskService
from source.services.greeting_service import GreetingService
from source.services.update_task_service import UpdateTaskService
from source.repositories.fake_task_repository import FakeTaskRepository

logger = logging.getLogger(__name__)


class Container(containers.DeclarativeContainer):
    greeting_service = providers.Singleton(GreetingService)
    task_repository = providers.Singleton(FakeTaskRepository)
    create_task_service = providers.Singleton(
        CreateTaskService, repository=task_repository
    )
    get_all_tasks_service = providers.Singleton(
        GetAllTasksService, repository=task_repository
    )
    get_task_service = providers.Singleton(GetTaskService, repository=task_repository)
    update_task_service = providers.Singleton(
        UpdateTaskService, repository=task_repository
    )
    delete_task_service = providers.Singleton(
        DeleteTaskService, repository=task_repository
    )


def setup_container() -> Container:
    logger.info("Setting up dependency injection container...")
    container = Container()
    _wire_controllers_by_container(container)
    logger.info("Dependency injection container wired successfully")
    return container


def _wire_controllers_by_container(container: Container) -> None:
    modules: List[str] = [
        info.name
        for info in pkgutil.walk_packages(
            path=source.controllers.__path__,
            prefix="source.controllers.",
        )
    ]
    container.wire(modules=modules)
