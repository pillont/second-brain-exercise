# Container & Dependency Injection Convention

## Auto-wiring controllers

Controllers are wired using `pkgutil.walk_packages` — never list them manually:

```python
import pkgutil
import source.controllers

def _wire_controllers_by_container(container: Container) -> None:
    modules = [
        info.name
        for info in pkgutil.walk_packages(
            path=source.controllers.__path__,
            prefix="source.controllers.",
        )
    ]
    container.wire(modules=modules)
```

## ISP — one class per operation

| Endpoint | Repository ABC | Service |
|---|---|---|
| `POST /tasks` | `CreateTaskRepository` | `CreateTaskService` |
| `GET /tasks` | `GetAllTasksRepository` | `GetAllTasksService` |
| `GET /tasks/{id}` | `GetTaskRepository` | `GetTaskService` |
| `PUT /tasks/{id}` | `UpdateTaskRepository` | `UpdateTaskService` |
| `DELETE /tasks/{id}` | `DeleteTaskRepository` | `DeleteTaskService` |
| `POST /auth/register` | `RegisterUserRepository` | `RegisterUserService` |
| `POST /auth/login` | `GetUserByUsernameRepository` | `LoginUserService` |

When adding a new operation, always create a new ABC in `repositories/` and a new service in `services/` — never extend an existing one.

Never disable pylint rules inline (`# pylint: disable=...`) — fix the root cause or configure the tool.

## ISP at container level

One provider per interface — never wire a single shared repository to all services:

```python
# WRONG — one repo shared by all services
task_repository = Singleton(TasksFakeRepository)
create_task_service = Singleton(CreateTaskService, repository=task_repository)
get_all_tasks_service = Singleton(GetAllTasksService, repository=task_repository)

# CORRECT — one provider per interface
create_task_repository = Singleton(CreateTaskSqlalchemyRepository, engine=sql_alchemy_engine)
get_all_tasks_repository = Singleton(GetAllTasksSqlalchemyRepository, engine=sql_alchemy_engine)
create_task_service = Singleton(CreateTaskService, repository=create_task_repository)
get_all_tasks_service = Singleton(GetAllTasksService, repository=get_all_tasks_repository)
```

## Selecting between SQLAlchemy and fake at runtime

Use `DATABASE_URL` presence in `AppConfig` to switch implementations. Testing config omits `DATABASE_URL` → fake is used automatically:

```python
def _select_repo(config: AppConfig, sql_repo: Callable[[], Any], fake_repo: Callable[[], Any]) -> Any:
    return sql_repo() if config.get("DATABASE_URL") else fake_repo()

create_task_repository = providers.Callable(
    _select_repo, config.provided, create_tasks_sql_alchemy_repo.provider, fake_tasks_repo.provider
)
```

## SQLAlchemy engine must be `providers.Singleton`

```python
# WRONG — Callable creates a new engine per repo → each has its own separate in-memory DB
sql_alchemy_engine = providers.Callable(get_sqlalchemy_engine, config=config.provided)

# CORRECT — Singleton ensures all repos share the same engine and connection pool
sql_alchemy_engine = providers.Singleton(get_sqlalchemy_engine, config=config.provided)
```
