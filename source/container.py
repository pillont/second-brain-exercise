import pkgutil
import logging

from sqlalchemy import create_engine
import source.controllers.v1
from typing import Any, Callable, List, cast
from dependency_injector import containers
from dependency_injector import providers
from source.config.app_config import AppConfig
from source.repositories.sqlalchemy.tasks.repositories\
    .create.create_task_sqlalchemy_repository import (
        CreateTaskSqlalchemyRepository,
    )
from source.repositories.sqlalchemy.tasks.repositories\
    .delete_task_sqlalchemy_repository import (
        DeleteTaskSqlalchemyRepository,
    )
from source.repositories.sqlalchemy.tasks.repositories\
    .get_all.get_all_tasks_sqlalchemy_repository import (
        GetAllTasksSqlalchemyRepository,
    )
from source.repositories.sqlalchemy.tasks.repositories\
    .get_task_sqlalchemy_repository import (
        GetTaskSqlalchemyRepository,
    )
from source.repositories.sqlalchemy.tasks.repositories\
    .update_task_sqlalchemy_repository import (
        UpdateTaskSqlalchemyRepository,
    )
from source.services.create_task_service import CreateTaskService
from source.services.delete_task_service import DeleteTaskService
from source.services.get_all_tasks_service import GetAllTasksService
from source.services.get_task_service import GetTaskService
from source.services.greeting_service import GreetingService
from source.services.login_user_service import LoginUserService
from source.services.register_user_service import RegisterUserService
from source.services.update_task_service import UpdateTaskService
from source.repositories.fake.tasks_fake_repository import TasksFakeRepository
from source.repositories.fake.users_fake_repository import FakeUserRepository

logger = logging.getLogger(__name__)


def _select_repo(
    config: AppConfig, sql_repo: Callable[[], Any], fake_repo: Callable[[], Any]
) -> Any:
    return sql_repo() if config.get("DATABASE_URL", None) else fake_repo()


def get_sqlalchemy_engine(config: AppConfig) -> Any:
    return create_engine(config["DATABASE_URL"])


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    greeting_service = providers.Singleton(GreetingService)

    fake_tasks_repo = providers.Singleton(TasksFakeRepository)

    sql_alchemy_engine = providers.Singleton(
        get_sqlalchemy_engine, config=config.provided
    )

    create_tasks_sql_alchemy_repo = providers.Singleton(
        CreateTaskSqlalchemyRepository, engine=sql_alchemy_engine
    )
    update_tasks_sql_alchemy_repo = providers.Singleton(
        UpdateTaskSqlalchemyRepository, engine=sql_alchemy_engine
    )
    delete_tasks_sql_alchemy_repo = providers.Singleton(
        DeleteTaskSqlalchemyRepository, engine=sql_alchemy_engine
    )
    get_tasks_sql_alchemy_repo = providers.Singleton(
        GetTaskSqlalchemyRepository, engine=sql_alchemy_engine
    )
    get_all_tasks_sql_alchemy_repo = providers.Singleton(
        GetAllTasksSqlalchemyRepository, engine=sql_alchemy_engine
    )

    create_task_repository = providers.Callable(
        _select_repo,
        config.provided,
        create_tasks_sql_alchemy_repo.provider,
        fake_tasks_repo.provider,
    )
    update_task_repository = providers.Callable(
        _select_repo,
        config.provided,
        update_tasks_sql_alchemy_repo.provider,
        fake_tasks_repo.provider,
    )
    delete_task_repository = providers.Callable(
        _select_repo,
        config.provided,
        delete_tasks_sql_alchemy_repo.provider,
        fake_tasks_repo.provider,
    )
    get_task_repository = providers.Callable(
        _select_repo,
        config.provided,
        get_tasks_sql_alchemy_repo.provider,
        fake_tasks_repo.provider,
    )
    get_all_tasks_repository = providers.Callable(
        _select_repo,
        config.provided,
        get_all_tasks_sql_alchemy_repo.provider,
        fake_tasks_repo.provider,
    )

    create_task_service = providers.Singleton(
        CreateTaskService, repository=create_task_repository
    )
    get_all_tasks_service = providers.Singleton(
        GetAllTasksService, repository=get_all_tasks_repository
    )
    get_task_service = providers.Singleton(
        GetTaskService, repository=get_task_repository
    )
    update_task_service = providers.Singleton(
        UpdateTaskService, repository=update_task_repository
    )
    delete_task_service = providers.Singleton(
        DeleteTaskService, repository=delete_task_repository
    )

    user_repository = providers.Singleton(FakeUserRepository)

    register_user_service = providers.Singleton(
        RegisterUserService, repository=user_repository
    )
    login_user_service = providers.Singleton(
        LoginUserService,
        repository=user_repository,
        config=config.provided,
    )


def setup_container(app_config: AppConfig) -> Container:
    logger.info("Setting up dependency injection container...")
    container = Container()
    container.config.from_dict(cast(dict, app_config))
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
