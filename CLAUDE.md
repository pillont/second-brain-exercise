# Project Instructions & Context

### Description
you can find the project description in [this file](./readme.md)

## Project Structure (MVC Architecture)

**Architecture Pattern**: 5-layer MVC with Flask
- See detailed documentation in [architecture.md](./source/architecture.md)

```
source/
├── app.py                   (entry point — init logger, run server)
├── create_app.py            (Flask app factory)
├── container.py             (dependency injection container)
├── config/
│   ├── __init__.py          ← empty, package marker only
│   └── config.py            (Config classes + get_config())
├── models/
│   ├── __init__.py
│   ├── task.py              (TaskStatus enum, TaskData, TaskUpdateData, Task)
│   ├── greeting.py          (Greeting)
│   └── not_found_error.py   (NotFoundError — raised by repositories when id not found)
├── repositories/
│   ├── __init__.py
│   ├── create_task_repository.py   (CreateTaskRepository ABC)
│   ├── get_all_tasks_repository.py (GetAllTasksRepository ABC)
│   ├── get_task_repository.py      (GetTaskRepository ABC)
│   ├── update_task_repository.py   (UpdateTaskRepository ABC)
│   ├── delete_task_repository.py   (DeleteTaskRepository ABC)
│   └── fake_task_repository.py     (in-memory implementation of all ABCs)
├── services/
│   ├── __init__.py
│   ├── greeting_service.py         (GreetingService)
│   ├── create_task_service.py      (CreateTaskService)
│   ├── get_all_tasks_service.py    (GetAllTasksService)
│   ├── get_task_service.py         (GetTaskService)
│   ├── update_task_service.py      (UpdateTaskService)
│   └── delete_task_service.py      (DeleteTaskService)
├── controllers/
│   ├── __init__.py
│   ├── greeting_controller.py
│   ├── tasks_controller.py  (POST, GET list, GET /{id}, PUT /{id}, DELETE /{id})
│   ├── schemas/              ← one file per schema
│   │   ├── __init__.py
│   │   ├── link_schema.py            (LinkSchema, LinksSchema — HATEOAS)
│   │   ├── task_data_schema.py       (TaskDataSchema — POST body)
│   │   ├── task_update_data_schema.py (TaskUpdateDataSchema — PUT body)
│   │   └── task_schema.py            (TaskSchema — response)
│   ├── entities/             ← one file per controller output DTO
│   │   ├── __init__.py
│   │   ├── link.py           (HttpMethod enum, LinkEntity, LinksEntity)
│   │   ├── greeting_entity.py
│   │   └── task_entity.py    (TaskDataEntity, TaskUpdateDataEntity, TaskLinks, TaskEntity)
│   ├── mappers/              ← one file per resource
│   │   ├── __init__.py
│   │   ├── greeting_mapper.py
│   │   └── task_mapper.py    (to_task_data, to_task_update_data, to_task_entity)
│   └── utils/
│       ├── error_handlers.py (centralized Flask error handler)
│       └── request_logger.py (before_request logger)
└── tests/
    ├── __init__.py
    ├── unit/
    │   ├── test_models/
    │   ├── test_services/
    │   ├── test_controllers/
    │   ├── test_repositories/
    │   └── test_utils/
    └── integration/
        └── test_tasks_controller.py
```


## Setup & Environment
- **Python Version**: 3.14.4
- **Environment**: venv (`/Users/thibautpillon/dev/python_env/.venv`)
- **Python Executable**: `/Users/thibautpillon/dev/python_env/.venv/bin/python`
- **Pip Command**: `/Users/thibautpillon/dev/python_env/.venv/bin/python -m pip`

### Installed Packages
- magicmock (for mocking in tests)
- pytest (unit testing framework)
- pytest-cov (coverage measurement)
- pytest-mock (mocking support)
- pytest-asyncio (async test support)
- mypy (static type checking)
- flake8 (style checker)
- black (code formatter)
- pylint (linter and code analysis)
- radon (complexity measurement)
- marshmallow (schema-based serialization)
- flask-smorest (annotation-based response serialization + OpenAPI)

### Serialization Pattern (flask-smorest + marshmallow)

Controllers **never** call `schema.dump()` manually. Instead, use the `@blp.response` decorator so flask-smorest serializes the return value automatically:

```python
from flask_smorest import Blueprint
from source.models.my_model import MyModel
from source.controllers.schemas.my_schema import MySchema

my_blp = Blueprint("my_resource", __name__, url_prefix="/my-resource")

@my_blp.route("/", methods=["GET"])
@my_blp.response(200, MySchema)
@inject
def get_resource(my_service=Provide[Container.my_service]) -> MyModel:
    return my_service.do_something()
```

- **One schema per file** in `source/controllers/schemas/` — naming convention: `<resource>_schema.py` → `class <Resource>Schema(Schema)`
- No need to instantiate the schema class (flask-smorest handles it)
- Blueprints must be registered via `api.register_blueprint()` (not `app.register_blueprint()`), where `api = Api(app)` in `create_app()`
- The `Config` base class must include `API_TITLE`, `API_VERSION`, and `OPENAPI_VERSION` for flask-smorest
- flask-smorest exposes `/openapi.json` and `/swagger-ui` automatically
- **No `# type: ignore`** — third-party packages without stubs are configured in `mypy.ini` with `ignore_missing_imports = True` per package section

## Development Standards

All agents developing for this project must follow these standards. Skills are automatically activated and provide detailed guidance:

### Code Quality Standards
- **PEP 8** — Python style guide (see `/python-pep8-conventions` skill)
  - Use snake_case for functions/variables, PascalCase for classes
  - Max line length: 88 characters
  - 4 spaces per indentation level
  - No comments `#` or docstrings `"""` in any `.py` file
  - Run `flake8 source/` to check style

- **Type Hints** — Python typing module (see `/python-typing` skill)
  - Annotate all function parameters and return types
  - Use `Optional[T]` for nullable values
  - Use generics for collections: `List[str]`, `Dict[str, int]`
  - Run `mypy source/` to validate types

- **Clean Code & SOLID** — Maintainability principles (see `/python-clean-code-solid` skill)
  - Single Responsibility Principle (SRP)
  - Open/Closed Principle (OCP)
  - Liskov Substitution Principle (LSP)
  - **Interface Segregation Principle (ISP)** — one interface per operation: `CreateTaskRepository`, not `TaskRepository`. Same for services: `CreateTaskService`.
  - Dependency Inversion Principle (DIP)
  - Maximum function length: 20 lines
  - Avoid code duplication (DRY)
  - Use dependency injection for testability
  - **Method ordering in classes**: `__init__` → public methods → private methods (`_`)
  - **Extract sub-functions** for distinct concerns: link building, entity mapping, blueprint registration, logger init
  - **Module-level logger**: `logger = logging.getLogger(__name__)` at the top of the file, after imports — never passed as a parameter

### Testing Standards
- **Unit Tests** — Test individual functions/methods (see `/python-unit-testing` skill)
  - Framework: pytest
  - Pattern: Arrange-Act-Assert (AAA)
  - Mock all external dependencies
  - Target: >80% code coverage
  - Run `pytest source/tests/unit/` to run unit tests

- **Integration Tests** — Test component interactions (see `/python-integration-testing` skill)
  - Mock external APIs + databases
  - Test feature workflows end-to-end
  - Test error scenarios (timeouts, API failures)
  - Use fixtures for shared setup
  - Run `pytest source/tests/integration/` to run integration tests

## Testing
<!-- How to run tests -->

### Running Tests Locally

```bash
# All tests
python -m pytest source/tests/ -v

# Unit tests only
python -m pytest source/tests/unit/ -v

# Integration tests only
python -m pytest source/tests/integration/ -v

# With coverage
python -m pytest source/tests/ --cov=source --cov-report=html

# Specific test
python -m pytest source/tests/unit/test_module.py::TestClass::test_method -v
```

### Code Quality Tools (Local Development)

```bash
# Style checking (PEP 8)
python -m flake8 source/

# Auto-format code
python -m black source/

# Type checking
python -m mypy source/

# Complexity analysis
python -m pylint source/ --disable=C0111
```

## `__init__.py` Convention

`__init__.py` files are **package markers only** — they must remain empty.

**Never put** class definitions, functions, variables, imports, comments, or docstrings in an `__init__.py`.

When a package needs shared code, create a named module instead:

| Package | Module for shared code |
|---|---|
| `source/config/` | `source/config/config.py` |
| `source/models/` | `source/models/my_model.py` |
| `source/services/` | `source/services/my_service.py` |

Consumers import from the named module directly:

```python
from source.config.config import Config, get_config
from source.models.greeting import Greeting
```

---

## HATEOAS & Controller Entities Pattern

All API responses follow HATEOAS — each response includes a `_links` object with hypermedia links describing available actions and the current resource.

### Separation of concerns

**Domain models** (`source/models/`) are pure and never carry hypermedia links.

**Controller entities** (`source/controllers/entities/`) are output DTOs, specific to the controller layer. They wrap the domain model data and add the `_links` field before the response is serialized.

**Mappers** (`source/controllers/mappers/`) handle the conversion between domain models and controller entities. Controllers delegate all mapping to them.

### File structure

| File | Purpose |
|---|---|
| `source/controllers/entities/link.py` | `Link` and `Links` dataclasses (shared by all controllers) |
| `source/controllers/entities/<resource>_entity.py` | DTO for a given resource |
| `source/controllers/schemas/link_schema.py` | `LinkSchema` and `LinksSchema` (shared by all schemas) |
| `source/controllers/schemas/<resource>_schema.py` | Schema for the entity, includes `_links` field |
| `source/controllers/mappers/<resource>_mapper.py` | `to_<resource>_entity()` and input mapping functions |

### `data_key` mapping convention

Marshmallow `data_key` is used to map Python attribute names to the JSON keys required by HATEOAS:

| Python attribute | JSON key | Reason |
|---|---|---|
| `self_link` | `"self"` | `self` is a Python naming convention — not a keyword but confusing |
| `links` | `"_links"` | HATEOAS standard prefix |

### Full example

**entities/link.py** (shared, do not duplicate):
```python
from enum import StrEnum
from typing import NotRequired, TypedDict

class HttpMethod(StrEnum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"

class LinkEntity(TypedDict):
    href: str
    type: NotRequired[HttpMethod]

class LinksEntity(TypedDict):
    self_link: LinkEntity
```

**entities/greeting_entity.py**:
```python
from typing import TypedDict
from source.controllers.entities.link import LinksEntity

class GreetingLinks(LinksEntity):
    pass

class GreetingEntity(TypedDict):
    id: int
    message: str
    links: GreetingLinks
```

**schemas/link_schema.py** (shared, do not duplicate):
```python
from marshmallow import Schema, fields

class LinkSchema(Schema):
    href = fields.Str(required=True)
    type = fields.Str(load_default=None)

class LinksSchema(Schema):
    self_link = fields.Nested(LinkSchema, data_key="self", required=True)
```

**schemas/greeting_schema.py**:
```python
from marshmallow import Schema, fields
from source.controllers.schemas.link_schema import LinksSchema

class GreetingLinksSchema(LinksSchema):
    pass

class GreetingSchema(Schema):
    id = fields.Int(required=True)
    message = fields.Str(required=True)
    links = fields.Nested(GreetingLinksSchema, data_key="_links", required=True)
```

**mappers/greeting_mapper.py** — builds links and maps to entity:
```python
from source.controllers.entities.link import LinkEntity
from source.controllers.entities.greeting_entity import GreetingEntity, GreetingLinks
from source.models.greeting import Greeting

def _build_links() -> GreetingLinks:
    return GreetingLinks(self_link=LinkEntity(href="/hello"))

def to_greeting_entity(greeting: Greeting) -> GreetingEntity:
    return GreetingEntity(id=greeting.id, message=greeting.message, links=_build_links())
```

**greeting_controller.py** — orchestrates only, no mapping logic:
```python
@greeting_blp.route("/hello", methods=["GET"])
@greeting_blp.response(200, GreetingSchema)
@inject
def get_greeting(greeting_service=Provide[Container.greeting_service]) -> GreetingEntity:
    return to_greeting_entity(greeting_service.get_greeting())
```

### TypedDict constructor pattern — never use `cast()`

Entities and links are `TypedDict`. Always use the constructor with keyword arguments — mypy resolves types at construction, making `cast()` unnecessary:

```python
return TaskLinks(
    self_link=LinkEntity(href=f"/tasks/{task.id}"),
    tasks=LinkEntity(href="/tasks/"),
    update=LinkEntity(href=f"/tasks/{task.id}", type=HttpMethod.PUT),
    delete=LinkEntity(href=f"/tasks/{task.id}", type=HttpMethod.DELETE),
)
```

Never use the dict literal + `cast()` pattern — it bypasses type checking:

```python
return cast(TaskLinks, {"self_link": {"href": "..."}})
```

### Task links reference

`TaskLinks` (in `task_entity.py`) currently exposes these links in every task response:

| Key | Method | href | Purpose |
|---|---|---|---|
| `self` | — | `/tasks/{id}` | The task itself |
| `tasks` | — | `/tasks/` | The task collection |
| `update` | `PUT` | `/tasks/{id}` | Update the task |
| `delete` | `DELETE` | `/tasks/{id}` | Delete the task |

### Rules

- **Never add `links` to a domain model** — models stay pure.
- **Never build links in a service or controller** — link building belongs in the mapper.
- **Never write mapping logic inline in a controller** — delegate to `<resource>_mapper.py`.
- **Reuse `link.py` and `link_schema.py`** — do not create new `LinkEntity`/`LinksEntity` classes per resource.
- **One entity file per resource** — naming: `<resource>_entity.py` → `class <Resource>Entity`.
- **One mapper file per resource** — naming: `<resource>_mapper.py`.
- **Never use `cast()`** — use the TypedDict constructor with kwargs instead.

---

## Error Handling & Request Logging Convention

**Controllers must NOT wrap endpoint logic in try/except.**

Two cross-cutting hooks are registered in `source/controllers/utils/` and wired in `create_app()`:

| File | Hook | Purpose |
|---|---|---|
| `error_handlers.py` | `@app.errorhandler(Exception)` | Catches all unhandled exceptions, logs at ERROR, returns HTTP 500 |
| `request_logger.py` | `@app.before_request` | Logs `METHOD /path` for every incoming request |

Because `request_logger.py` handles request logging globally, **controllers must not log the incoming request themselves**.

**Correct controller pattern:**
```python
@blueprint.route("/example", methods=["GET"])
@inject
def get_example(my_service=Provide[Container.my_service]) -> MyEntity:
    result = my_service.do_something()
    return to_my_entity(result)
```

Services and repositories may still raise domain-specific exceptions — the global handler will catch anything that bubbles up uncaught.

---

## Models Convention

- Use `StrEnum` (Python 3.11+) for status/type enums — guarantees `str(value) == value.value`, required for marshmallow `fields.Str()` serialization:

```python
from enum import StrEnum

class TaskStatus(StrEnum):
    INCOMPLETE = "Incomplete"
    COMPLETE = "Complete"
```

- Never use `str, Enum` — in Python 3.11+, `str()` returns `"ClassName.MEMBER"` not the value.

---

## Container & Dependency Injection Convention

Controllers are **auto-wired** using `pkgutil.walk_packages` — never list them manually:

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

ISP applies to repositories and services — one class per operation:

| Endpoint | Repository ABC | Service |
|---|---|---|
| `POST /tasks` | `CreateTaskRepository` | `CreateTaskService` |
| `GET /tasks` | `GetAllTasksRepository` | `GetAllTasksService` |
| `GET /tasks/{id}` | `GetTaskRepository` | `GetTaskService` |
| `PUT /tasks/{id}` | `UpdateTaskRepository` | `UpdateTaskService` |
| `DELETE /tasks/{id}` | `DeleteTaskRepository` | `DeleteTaskService` |

When adding a new operation, always create a new ABC in `repositories/` and a new service in `services/` — never extend an existing one.

Never disable pylint rules inline (`# pylint: disable=...`) — fix the root cause or configure the tool.

---

## CI/CD Pipeline

### GitHub Actions Workflow

A **continuous integration workflow** automatically runs quality checks on every push and pull request.

**Workflow file**: `.github/workflows/quality-checks.yml`

**Triggered on**:
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop` branches

**Checks performed** (in order):
1. **Black formatting** — Ensure consistent code format
2. **Flake8 (PEP 8)** — Python style compliance
3. **MyPy** — Type hint validation
4. **Unit Tests** — Run with >80% coverage requirement
5. **Integration Tests** — Component interaction testing
6. **Radon complexity** — Code complexity analysis
7. **Pylint** — Additional code issues
8. **Coverage report** — Artifacts uploaded for review

**Status**: 
- ✅ All checks must pass before PR merge
- 📊 Coverage reports available in artifacts

See [CI/CD Workflow Guide](.claude/commands/python-pep8-conventions-references/ci-cd-workflow.md) for details.

### Pre-commit Hooks (Optional Local)

Set up local pre-commit hooks to catch issues before pushing.

**Installation**:
```bash
pip install pre-commit
pre-commit install
```

**Configuration**: `.pre-commit-config.yaml`
- Runs Black formatter
- Runs Flake8 checker
- Runs MyPy type checker
- Cleans trailing whitespace
- Fixes file endings

**Usage**:
```bash
# Hooks run automatically on git commit
git commit -m "my changes"  # Hooks execute here

# Manual run
pre-commit run --all-files

# Skip (not recommended)
git commit --no-verify
```

See [CI/CD Workflow Guide](.claude/commands/python-pep8-conventions-references/ci-cd-workflow.md) for detailed instructions.