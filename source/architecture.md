# Architecture and MVC Layers

This document describes the 5-layer MVC architecture used in this Flask Task Management API.

## Getting Started

### Running the API

**Option 1 — VS Code (recommended)**: press **F5** (Run & Debug). The server starts and the Swagger UI opens automatically in the browser via the `serverReadyAction` configured in `.vscode/launch.json`.

**Option 2 — terminal**: always run from the project root using `-m` (never `python source/app.py` — the `source` package won't resolve):
```bash
.venv/bin/python -m source.app
```

The API runs on **http://127.0.0.1:5001** (port 5001 — port 5000 is occupied by macOS AirPlay Receiver).

Swagger UI: **http://127.0.0.1:5001/swagger-ui**

### Swagger UI Configuration

flask-smorest requires these three keys in `Config` to expose the Swagger UI:

```python
OPENAPI_URL_PREFIX = "/"
OPENAPI_SWAGGER_UI_PATH = "/swagger-ui"
OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
```

They are defined in `source/config/__init__.py` on the base `Config` class and inherited by all environments.

### First Endpoint: GET /hello

This is the first example endpoint that demonstrates the complete 5-layer architecture:

```bash
curl http://127.0.0.1:5001/hello
```

Response:
```json
{
  "id": 1,
  "message": "Hello from API!"
}
```

**Architecture Flow**:
1. **Controller** (`greeting_controller.py`) receives the HTTP GET request on `/hello`
2. **Service** (`greeting_service.py`) executes business logic and returns a `Greeting` object
3. **Model** (`models/greeting.py`) defines the `Greeting` domain entity
4. **Schema** (`controllers/schemas/greeting_schema.py`) defines `GreetingSchema`; flask-smorest uses it automatically via `@greeting_blp.response(200, GreetingSchema)` to serialize the model to JSON

### Configuration & Environment

The application uses environment-based configuration defined in `source/config.py`:

- **Development**: Debug mode enabled, logging at INFO level (default)
- **Testing**: Debug disabled, logging at WARNING level
- **Production**: Debug disabled, logging at INFO level

Set the environment:
```bash
export FLASK_ENV=development  # or testing, production
python -m source.app
```

### Logging

The application logs all activity with timestamps and severity levels:

```
%(asctime)s - %(name)s - %(levelname)s - %(message)s
```

Example:
```
2026-04-29 10:15:30,127 - source - INFO - Creating Flask app in 'development' mode
2026-04-29 10:15:30,128 - source.controllers.greeting_controller - INFO - GET /hello endpoint called
2026-04-29 10:15:30,129 - source.services.greeting_service - INFO - GreetingService.get_greeting() called
```

Logs are output to stdout and can be redirected to files if needed.

### Factory Pattern

The application uses the **Flask Application Factory Pattern** for flexible configuration and testability:

- **Advantages**:
  - Create multiple app instances for different configurations
  - Easy testing with different configurations per test
  - Scalable for complex applications
  - Clean separation of concerns

- **Implementation**:
  - `source/__init__.py` contains the `create_app(config_name)` factory function
  - `source/app.py` calls the factory to create the app instance
  - This allows easy configuration switching without code changes

### Dependency Injection with dependency-injector

The application uses the **dependency-injector** library for professional-grade dependency management:

- **Library**: `dependency-injector==4.41.0`
- **Container**: Defined in `source/container.py` as a `DeclarativeContainer`
- **Services**: Declared as `providers.Singleton()` for single instance per application

**How it works**:

1. **Define services** in `source/container.py`:
```python
class Container(containers.DeclarativeContainer):
    greeting_service = providers.Singleton(GreetingService)
```

2. **Wire container** during app initialization in `source/__init__.py`:
```python
app.container = setup_container()  # Wires all modules
```

3. **Inject services** in controller functions:
```python
from dependency_injector.wiring import inject, Provide
from source.container import Container

@inject
def get_greeting(greeting_service=Provide[Container.greeting_service]):
    return greeting_service.get_greeting()
```

**Benefits**:
- ✅ Services are singletons (single instance per app)
- ✅ Dependencies are centralized in one container
- ✅ Easy to test (swap services in test container)
- ✅ No manual instantiation or parameter passing
- ✅ Clean and declarative approach

**Pattern for new services**:
```python
# 1. Add service class in source/services/my_service.py
class MyService:
    def do_something(self):
        pass

# 2. Register in source/container.py
class Container(containers.DeclarativeContainer):
    my_service = providers.Singleton(MyService)
    greeting_service = providers.Singleton(GreetingService)

# 3. Wire the module in setup_container()
container.wire(modules=['source.controllers.my_controller'])

# 4. Inject in controller
@inject
def my_endpoint(my_service=Provide[Container.my_service]):
    return my_service.do_something()
```

---

## Overview

The application follows a **5-layer MVC architecture** designed to maintain clear separation of concerns and facilitate testing, maintenance, and scalability.

```
Request
  ↓
[CONTROLLERS] - Route handlers, HTTP endpoints, request/response mapping
  ↓
[SERVICES] - Business logic, validation, orchestration
  ↓
[REPOSITORIES] - Data access, database queries, persistence
  ↓
[MODELS] - Domain entities, data validation
  ↓
Response
```

---

## Layer Responsibilities

### 1. **Controllers** (`source/controllers/`)
**Purpose**: Handle HTTP requests and responses, define API endpoints

**Responsibilities**:
- Define Flask blueprints and routes
- Receive user input from requests
- Validate HTTP parameters (query strings, JSON body)
- Inject and call appropriate service methods
- Format and return JSON responses with proper HTTP status codes
- Handle request/response serialization
- Use `@inject` decorator to receive services as parameters

**Pattern**:
```python
import logging
from flask_smorest import Blueprint  # type: ignore[import-untyped]
from dependency_injector.wiring import inject, Provide
from source.container import Container
from source.models.my_model import MyModel
from source.controllers.schemas.my_schema import MySchema

logger = logging.getLogger(__name__)

my_blp = Blueprint("my_resource", __name__, url_prefix="/my-resource")


@my_blp.route("/", methods=["GET"])
@my_blp.response(200, MySchema)
@inject
def get_resource(
    my_service=Provide[Container.my_service],
) -> MyModel:
    logger.info("GET /my-resource called")
    return my_service.do_something()
```

**How serialization works**:
- `@my_blp.response(200, MySchema)` is a flask-smorest decorator that wraps the view function
- The function returns the domain model object directly (e.g. `Greeting`, `Task`)
- flask-smorest calls `MySchema().dump(result)` automatically and serializes to JSON
- Never call `schema.dump()` manually in a controller
- Each schema lives in its own file under `source/controllers/schemas/<resource>_schema.py` (e.g. `greeting_schema.py` → `GreetingSchema`)

**Rules**:
- No try/except — unexpected errors are handled globally by `utils/error_handlers.py`
- Always use `@inject` with `Provide[Container.service]` for service injection
- Always annotate responses with `@blp.response(status_code, SchemaClass)` — never serialize manually
- Return the domain model object directly, not a dict or tuple
- Log at entry point
- Register the blueprint via `api.register_blueprint()` in `source/__init__.py` and wire its module in `source/container.py`

**Implemented endpoints**:

| Method | Path | Status code | Description |
|---|---|---|---|
| `GET` | `/hello` | 200 | Greeting example |
| `POST` | `/tasks/` | 201 | Create a task |
| `GET` | `/tasks/` | 200 | List all tasks |
| `GET` | `/tasks/{id}` | 200 / 404 | Get a task by id |
| `PUT` | `/tasks/{id}` | 204 / 404 | Update a task |
| `DELETE` | `/tasks/{id}` | 204 / 404 | Delete a task |

**Files**:
- `greeting_controller.py` - GET /hello
- `tasks_controller.py` - Full task CRUD (POST, GET list, GET by id, PUT, DELETE)
- `schemas/` - One schema file per resource (`<resource>_schema.py`)
- `entities/` - Output DTOs + HATEOAS link types
- `mappers/` - Mapping from domain models to entities
- `utils/error_handlers.py` - Global exception handler → HTTP 500
- `utils/request_logger.py` - Before-request logger

**Dependencies**: Services

---

### 2. **Services** (`source/services/`)
**Purpose**: Encapsulate business logic and orchestration

**Responsibilities**:
- Implement business logic methods (non-static instance methods)
- Validate business rules (e.g., task status validity)
- Orchestrate multiple repository calls
- Implement complex workflows (e.g., user registration with validation)
- Apply security rules (e.g., only task owner can delete)
- Handle error scenarios with meaningful messages
- Manage transactions and consistency

**Pattern**:
```python
class GreetingService:
    def get_greeting(self):
        # Business logic here
        pass
```

**Dependency Injection in Services**:
Services can receive other dependencies (repositories, utils) via constructor:
```python
class TaskService:
    def __init__(self, task_repository):
        self.task_repository = task_repository
    
    def get_task(self, task_id):
        return self.task_repository.find_by_id(task_id)
```

Then register in container:
```python
class Container(containers.DeclarativeContainer):
    task_repository = providers.Singleton(TaskRepository)
    task_service = providers.Singleton(
        TaskService,
        task_repository=task_repository
    )
```

**Files**:
- `greeting_service.py` - GreetingService
- `create_task_service.py` - CreateTaskService
- `get_all_tasks_service.py` - GetAllTasksService
- `get_task_service.py` - GetTaskService
- `update_task_service.py` - UpdateTaskService
- `delete_task_service.py` - DeleteTaskService

**Dependencies**: Repositories, Models, Utils

---

### 3. **Repositories** (`source/repositories/`)
**Purpose**: Abstract data access and provide a clean interface to persistence

**Responsibilities**:
- Query the database (or any data source)
- Create, read, update, delete operations
- Handle SQL queries or ORM operations
- Manage connection pooling and transaction boundaries
- Provide reusable query patterns (filtering, sorting, pagination)
- Return model instances (never raw database rows)

**Files** (ISP — one ABC per operation):
- `create_task_repository.py` - CreateTaskRepository ABC
- `get_all_tasks_repository.py` - GetAllTasksRepository ABC
- `get_task_repository.py` - GetTaskRepository ABC
- `update_task_repository.py` - UpdateTaskRepository ABC
- `delete_task_repository.py` - DeleteTaskRepository ABC
- `fake_task_repository.py` - In-memory implementation of all ABCs (used in tests and dev)

**Dependencies**: Models, Config

---

### 4. **Models** (`source/models/`)
**Purpose**: Define domain entities and validation rules

**Responsibilities**:
- Define Task, User, and other domain objects
- Implement data validation (Pydantic models or dataclasses)
- Define serialization/deserialization rules
- Document required fields and constraints
- Provide type hints for IDE support

**Files**:
- `task.py` - TaskStatus (StrEnum), TaskData, TaskUpdateData, Task
- `greeting.py` - Greeting
- `not_found_error.py` - NotFoundError (raised by repositories, caught by global error handler → 404)

> **Note**: Schemas live in `source/controllers/schemas/`, not here. See the Controllers section.

**Dependencies**: None (except standard library/Pydantic)

---

### 5. **Config** (`source/config/`)
**Purpose**: Centralize application configuration and settings

**Responsibilities**:
- Define Flask app configuration (debug mode, secret keys, database URL)
- Store environment variables
- Define application constants (max retries, timeouts)
- Configure logging levels
- Manage database connection settings

**Files**:
- `settings.py` - Base configuration settings
- `development.py` - Development-specific settings
- `production.py` - Production-specific settings
- `__init__.py` - Config initialization

**Dependencies**: None

---

## Supporting Layers

### 6. **Utils** (`source/utils/`)
**Purpose**: Provide shared utilities and helpers

**Responsibilities**:
- Decorators (e.g., authentication required, error handling)
- Helper functions (e.g., password hashing, JWT encoding/decoding)
- Middleware (e.g., request logging, CORS handling)
- Validators and formatters
- Common constants and enums

**Files**:
- `error_handlers.py` - Centralized Flask error handler (registered in `create_app`)
- `auth_utils.py` - JWT and password utilities
- `validators.py` - Input validation helpers
- `decorators.py` - Flask decorators
- `__init__.py` - Utilities exports

**Dependencies**: None (except standard library)

---

### 7. **Tests** (`source/tests/`)
**Purpose**: Organize unit and integration tests

**Structure**:
```
tests/
├── unit/
│   ├── test_models/
│   ├── test_services/
│   ├── test_controllers/
│   └── test_repositories/
└── integration/ (optional)
    └── test_api_flow.py
```

**Responsibilities**:
- Test individual components in isolation
- Mock external dependencies (database, external APIs)
- Test integration between layers
- Verify error handling and edge cases

---

## Data Flow Examples

**POST /tasks — create a task**:
```
1. HTTP POST /tasks/ with JSON body
   ↓
2. [Controller] create_task()
   - flask-smorest deserializes body via TaskDataSchema → TaskDataEntity
   - Calls to_task_data() mapper → TaskData domain object
   - Calls CreateTaskService.create_task(task_data)
   ↓
3. [Service] CreateTaskService.create_task()
   - Delegates to CreateTaskRepository.create(task_data)
   - Returns Task model
   ↓
4. [Repository] FakeTaskRepository.create()
   - Assigns auto-incremented id, sets status=INCOMPLETE
   - Returns Task
   ↓
5. [Controller] calls to_task_entity(task) → TaskEntity with _links
   - flask-smorest serializes via TaskSchema → JSON
   - Returns HTTP 201
```

**DELETE /tasks/{id} — delete a task**:
```
1. HTTP DELETE /tasks/42
   ↓
2. [Controller] delete_task(id=42)
   - Calls DeleteTaskService.delete_task(42)
   ↓
3. [Service] DeleteTaskService.delete_task()
   - Delegates to DeleteTaskRepository.delete_task(42)
   ↓
4. [Repository] FakeTaskRepository.delete_task()
   - Finds task by id (raises NotFoundError if missing → 404)
   - Removes task from in-memory list
   ↓
5. [Controller] Returns HTTP 204 (no body)
```

---

## Dependency Injection Pattern

To maintain loose coupling, use dependency injection:

```python
# source/__init__.py
from flask_smorest import Api  # type: ignore[import-untyped]
from source.controllers.my_controller import my_blp

def create_app(config_obj):
    app = FlaskApp(__name__)
    app.config.from_object(config_obj)

    app.container = setup_container()

    # flask-smorest Api wraps the app and handles blueprint registration,
    # JSON serialization via @blp.response, and OpenAPI spec generation
    api = Api(app)
    api.register_blueprint(my_blp)

    register_error_handlers(app)
    return app
```

**Why `api.register_blueprint()` instead of `app.register_blueprint()`**: flask-smorest needs to intercept blueprint registration to wire up schema-based serialization and generate the OpenAPI spec. Always go through the `Api` object.

---

## Testing Strategy

### Unit Tests
- Test each layer independently
- Mock dependencies
- Focus on business logic

Example:
```python
# tests/unit/test_services/test_task_service.py
def test_create_task_validates_title():
    mock_repo = Mock()
    service = TaskService(mock_repo)
    
    with pytest.raises(ValidationError):
        service.create_task(title="", description="test")
```

### Integration Tests
- Test layers working together
- Use test database
- Verify end-to-end flow

---

## Guidelines

1. **Never skip layers**: Controllers must call Services, Services must call Repositories
2. **Keep layers thin**: Move complexity to Services
3. **Reuse across layers**: Share Model definitions, use them everywhere
4. **Error handling**: Controllers must NOT use try/except — unexpected exceptions bubble up to the global handler in `utils/error_handlers.py` which logs them and returns HTTP 500. Services and repositories may raise domain exceptions freely.
5. **Logging**: Add at layer boundaries and in Services
6. **No circular dependencies**: Flow is always downward (Controllers → Services → Repositories → Models)

---

## File Organization Summary

```
source/
├── app.py
├── create_app.py
├── container.py
├── config/
│   └── config.py
├── models/
│   ├── task.py
│   ├── greeting.py
│   └── not_found_error.py
├── repositories/
│   ├── create_task_repository.py
│   ├── get_all_tasks_repository.py
│   ├── get_task_repository.py
│   ├── update_task_repository.py
│   ├── delete_task_repository.py
│   └── fake_task_repository.py
├── services/
│   ├── greeting_service.py
│   ├── create_task_service.py
│   ├── get_all_tasks_service.py
│   ├── get_task_service.py
│   ├── update_task_service.py
│   └── delete_task_service.py
├── controllers/
│   ├── greeting_controller.py
│   ├── tasks_controller.py
│   ├── schemas/
│   │   ├── link_schema.py
│   │   ├── task_data_schema.py
│   │   ├── task_update_data_schema.py
│   │   └── task_schema.py
│   ├── entities/
│   │   ├── link.py
│   │   ├── greeting_entity.py
│   │   └── task_entity.py
│   ├── mappers/
│   │   ├── greeting_mapper.py
│   │   └── task_mapper.py
│   └── utils/
│       ├── error_handlers.py
│       └── request_logger.py
└── tests/
    ├── unit/
    │   ├── test_models/
    │   ├── test_services/
    │   ├── test_controllers/
    │   ├── test_repositories/
    │   └── test_utils/
    └── integration/
        └── test_tasks_controller.py
```
