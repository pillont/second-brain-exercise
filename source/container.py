import pkgutil
import logging
import source.controllers
from typing import List
from dependency_injector import containers
from dependency_injector.providers import Configuration, Singleton
from source.config.app_config import AppConfig
from source.services.create_task_service import CreateTaskService
from source.services.delete_task_service import DeleteTaskService
from source.services.get_all_tasks_service import GetAllTasksService
from source.services.get_task_service import GetTaskService
from source.services.greeting_service import GreetingService
from source.services.login_user_service import LoginUserService
from source.services.register_user_service import RegisterUserService
from source.services.update_task_service import UpdateTaskService
from source.repositories.fake_task_repository import FakeTaskRepository
from source.repositories.fake_user_repository import FakeUserRepository

logger = logging.getLogger(__name__)


class Container(containers.DeclarativeContainer):
    config = Configuration()
    greeting_service = Singleton(GreetingService)
    task_repository = Singleton(FakeTaskRepository)
    create_task_service = Singleton(CreateTaskService, repository=task_repository)
    get_all_tasks_service = Singleton(GetAllTasksService, repository=task_repository)
    get_task_service = Singleton(GetTaskService, repository=task_repository)
    update_task_service = Singleton(UpdateTaskService, repository=task_repository)
    delete_task_service = Singleton(DeleteTaskService, repository=task_repository)
    user_repository = Singleton(FakeUserRepository)
    register_user_service = Singleton(RegisterUserService, repository=user_repository)
    login_user_service = Singleton(
        LoginUserService,
        repository=user_repository,
        config=config,
    )


def setup_container(app_config: AppConfig) -> Container:
    logger.info("Setting up dependency injection container...")
    container = Container()
    container.config.from_object(app_config)
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
