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
