# Project Instructions & Context

### Description
you can find the project description in [this file](./readme.md)

## Project Structure (MVC Architecture)

**Architecture Pattern**: 5-layer MVC with Flask
- See detailed documentation in [architecture.md](./source/architecture.md)

```
source/
├── app.py (Flask application factory)
├── config/
│   ├── __init__.py          ← empty, package marker only
│   └── config.py            (Config classes + get_config())
├── models/
│   ├── __init__.py
│   ├── task.py (Task entity model)
│   └── user.py (User entity model)
├── repositories/
│   ├── __init__.py
│   ├── base_repository.py (common repository patterns)
│   ├── task_repository.py (Task data access)
│   └── user_repository.py (User data access)
├── services/
│   ├── __init__.py
│   ├── task_service.py (Task business logic)
│   └── user_service.py (User business logic & authentication)
├── controllers/
│   ├── __init__.py
│   ├── tasks_controller.py (Task API endpoints)
│   ├── users_controller.py (User API endpoints & auth)
│   ├── schemas/              ← one file per schema
│   │   ├── __init__.py
│   │   ├── link_schema.py (LinkSchema, LinksSchema — HATEOAS)
│   │   └── greeting_schema.py (GreetingSchema)
│   └── entities/             ← one file per controller output DTO
│       ├── __init__.py
│       ├── link.py (Link, Links — HATEOAS dataclasses)
│       └── greeting_entity.py (GreetingEntity)
├── utils/
│   ├── __init__.py
│   ├── error_handlers.py (centralized Flask error handler)
│   ├── auth_utils.py (JWT & password utilities)
│   ├── validators.py (validation helpers)
│   └── decorators.py (Flask decorators)
└── tests/
    ├── __init__.py
    └── unit/
        ├── test_models/ (model unit tests)
        ├── test_services/ (service unit tests)
        ├── test_controllers/ (controller unit tests)
        ├── test_repositories/ (repository unit tests)
        └── test_utils/ (utils unit tests)
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
from flask_smorest import Blueprint  # type: ignore[import-untyped]
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
- Add `# type: ignore[import-untyped]` on `from flask_smorest import ...` lines (no type stubs available)

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
  - Interface Segregation Principle (ISP)
  - Dependency Inversion Principle (DIP)
  - Maximum function length: 20 lines
  - Avoid code duplication (DRY)
  - Use dependency injection for testability

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

The controller is responsible for the mapping: `Model → Entity`.

### File structure

| File | Purpose |
|---|---|
| `source/controllers/entities/link.py` | `Link` and `Links` dataclasses (shared by all controllers) |
| `source/controllers/entities/<resource>_entity.py` | DTO for a given resource |
| `source/controllers/schemas/link_schema.py` | `LinkSchema` and `LinksSchema` (shared by all schemas) |
| `source/controllers/schemas/<resource>_schema.py` | Schema for the entity, includes `_links` field |

### `data_key` mapping convention

Marshmallow `data_key` is used to map Python attribute names to the JSON keys required by HATEOAS:

| Python attribute | JSON key | Reason |
|---|---|---|
| `self_link` | `"self"` | `self` is a Python naming convention — not a keyword but confusing |
| `links` | `"_links"` | HATEOAS standard prefix |

### Full example

**entities/link.py** (shared, do not duplicate):
```python
from dataclasses import dataclass

@dataclass
class Link:
    href: str

@dataclass
class Links:
    self_link: Link
```

**entities/greeting_entity.py**:
```python
from dataclasses import dataclass
from source.controllers.entities.link import Links

@dataclass
class GreetingEntity:
    id: int
    message: str
    links: Links
```

**schemas/link_schema.py** (shared, do not duplicate):
```python
from marshmallow import Schema, fields

class LinkSchema(Schema):
    href = fields.Str(required=True)

class LinksSchema(Schema):
    self_link = fields.Nested(LinkSchema, data_key="self", required=True)
```

**schemas/greeting_schema.py**:
```python
from marshmallow import Schema, fields
from source.controllers.schemas.link_schema import LinksSchema

class GreetingSchema(Schema):
    id = fields.Int(required=True)
    message = fields.Str(required=True)
    links = fields.Nested(LinksSchema, data_key="_links", required=True)
```

**greeting_controller.py** — the controller maps Model → Entity and injects the links:
```python
@greeting_blp.route("/hello", methods=["GET"])
@greeting_blp.response(200, GreetingSchema)
@inject
def get_greeting(greeting_service=Provide[Container.greeting_service]) -> GreetingEntity:
    greeting = greeting_service.get_greeting()
    links = Links(self_link=Link(href="/hello"))
    return GreetingEntity(id=greeting.id, message=greeting.message, links=links)
```

### Rules

- **Never add `links` to a domain model** — models stay pure.
- **Never build links in a service** — link building is a controller concern (URLs are HTTP layer knowledge).
- **Reuse `link.py` and `link_schema.py`** — do not create new `Link`/`Links` classes per resource.
- **One entity file per resource** — naming: `<resource>_entity.py` → `class <Resource>Entity`.

---

## Error Handling Convention

**Controllers must NOT wrap endpoint logic in try/except.**

All unexpected exceptions are caught and logged by a single global handler registered in `source/utils/error_handlers.py`. It:
- Logs every unhandled exception at `ERROR` level with full traceback
- Returns `{"error": "Internal server error"}` with HTTP 500
- Lets `HTTPException` (404, 405, etc.) pass through normally

The handler is registered in `create_app()` (`source/create_app.py`) and applies to every blueprint automatically.

**Correct controller pattern:**
```python
@blueprint.route("/example", methods=["GET"])
@inject
def get_example(my_service=Provide[Container.my_service]) -> tuple[dict, int]:
    logger.info("GET /example called")
    result = my_service.do_something()
    return schema.dump(result), 200
```

Services and repositories may still raise domain-specific exceptions — the global handler will catch anything that bubbles up uncaught.

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