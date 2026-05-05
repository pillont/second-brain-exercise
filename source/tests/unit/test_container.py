from source.container import Container
from source.repositories.fake.tasks_fake_repository import TasksFakeRepository
from source.repositories.sqlalchemy.tasks.repositories.create.create_task_sqlalchemy_repository import \
    CreateTaskSqlalchemyRepository
from source.repositories.sqlalchemy.tasks.repositories.delete_task_sqlalchemy_repository import \
    DeleteTaskSqlalchemyRepository
from source.repositories.sqlalchemy.tasks.repositories.get_all.get_all_tasks_sqlalchemy_repository import \
    GetAllTasksSqlalchemyRepository
from source.repositories.sqlalchemy.tasks.repositories.get_task_sqlalchemy_repository import \
    GetTaskSqlalchemyRepository
from source.repositories.sqlalchemy.tasks.repositories.update_task_sqlalchemy_repository import \
    UpdateTaskSqlalchemyRepository


def _get_container(is_fake: bool) -> Container:
    container = Container()

    container.config.from_dict(
        {"DATABASE_URL": "sqlite:///:memory:"} if not is_fake else {}
    )
    return container


def test_container_with_fake_config_should_return_fake_create_task_repository():
    container = _get_container(True)
    repo = container.create_task_repository()

    assert isinstance(repo, TasksFakeRepository)


def test_container_with_fake_config_should_return_fake_get_task_repository():
    container = _get_container(True)
    repo = container.get_task_repository()

    assert isinstance(repo, TasksFakeRepository)


def test_container_with_fake_config_should_return_fake_get_all_task_repository():
    container = _get_container(True)
    repo = container.get_all_tasks_repository()

    assert isinstance(repo, TasksFakeRepository)


def test_container_with_fake_config_should_return_fake_update_task_repository():
    container = _get_container(True)
    repo = container.update_task_repository()

    assert isinstance(repo, TasksFakeRepository)


def test_container_with_fake_config_should_return_fake_delete_task_repository():
    container = _get_container(True)
    repo = container.delete_task_repository()

    assert isinstance(repo, TasksFakeRepository)


def test_container_with_fake_config_should_return_same_fake_repository():
    container = _get_container(is_fake=True)
    create_repo = container.create_task_repository()
    get_repo = container.get_task_repository()
    get_all_repo = container.get_all_tasks_repository()
    update_repo = container.update_task_repository()
    delete_repo = container.delete_task_repository()

    assert create_repo == get_repo == get_all_repo == update_repo == delete_repo


def test_container_with_sql_config_should_return_fake_create_task_repository():
    container = _get_container(is_fake=False)
    repo = container.create_task_repository()

    assert isinstance(repo, CreateTaskSqlalchemyRepository)


def test_container_with_sql_config_should_return_fake_get_task_repository():
    container = _get_container(is_fake=False)
    repo = container.get_task_repository()

    assert isinstance(repo, GetTaskSqlalchemyRepository)


def test_container_with_sql_config_should_return_fake_get_all_task_repository():
    container = _get_container(is_fake=False)
    repo = container.get_all_tasks_repository()

    assert isinstance(repo, GetAllTasksSqlalchemyRepository)


def test_container_with_sql_config_should_return_fake_update_task_repository():
    container = _get_container(is_fake=False)
    repo = container.update_task_repository()

    assert isinstance(repo, UpdateTaskSqlalchemyRepository)


def test_container_with_sql_config_should_return_fake_delete_task_repository():
    container = _get_container(is_fake=False)
    repo = container.delete_task_repository()

    assert isinstance(repo, DeleteTaskSqlalchemyRepository)
