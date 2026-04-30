# Project Instructions & Context

### Description
See [readme.md](./readme.md)

## Project Structure (MVC Architecture)

**Architecture Pattern**: 5-layer MVC with Flask — see [project-structure](.claude/commands/project-structure.md) for the full file tree.

```
source/
├── config/        (AppConfig TypedDict, FlaskConfig subclasses)
├── models/        (domain models, StrEnum, error types)
├── repositories/  (ABCs + in-memory implementations)
├── services/      (one service class per operation)
├── controllers/   (blueprints, schemas, entities, mappers, utils)
└── tests/         (unit/ + integration/)
```

## Setup & Environment

- **Python**: 3.14.4 — venv at `.venv/`
- **Python executable**: `/Users/thibautpillon/dev/python_env/.venv/bin/python`
- **Pip**: `/Users/thibautpillon/dev/python_env/.venv/bin/python -m pip`

**Key non-obvious packages** (see `requirements.txt` for the full list):
- `flask-smorest` — `@blp.response` serialization + OpenAPI (see [serialization](.claude/commands/serialization.md))
- `flask-jwt-extended` — `@jwt_required()` route protection
- `werkzeug` — `generate_password_hash` / `check_password_hash`
- `dependency-injector` — `@inject` + `Provide[Container.x]`

## Development Standards

- **PEP 8** — snake_case functions/vars, PascalCase classes, 88 chars max (see `/python-pep8-conventions` skill)
- **No comments `#` or docstrings `"""`** in any `.py` file
- **Type hints** on all parameters and return types (see `/python-typing` skill)
- **SOLID / Clean Code** — see `/python-clean-code-solid` skill
  - ISP: one interface per operation (`CreateTaskRepository`, not `TaskRepository`) — same for services
  - Method ordering: `__init__` → public → private (`_`)
  - Module-level logger: `logger = logging.getLogger(__name__)` after imports, never passed as parameter
- **No `# pylint: disable`** inline — fix root cause or configure the tool

## Testing

```bash
python -m pytest source/tests/ -v
python -m pytest source/tests/unit/ -v
python -m pytest source/tests/integration/ -v
python -m pytest source/tests/ --cov=source --cov-report=html
```

```bash
python -m flake8 source/
python -m black source/
python -m mypy source/
python -m pylint source/ --disable=C0111
```

---

## Conventions

### `__init__.py`
Package markers only — must remain **empty**. Never put code, imports, or comments in `__init__.py`.

### HATEOAS
- All responses include a `_links` object — models stay pure, links belong in mappers only
- Never write mapping logic inline in a controller — delegate to `<resource>_mapper.py`
- Never use `cast()` on TypedDict — use the constructor with keyword arguments

See [hateoas](.claude/commands/hateoas.md) for full examples.

### Configuration
- `AppConfig` (TypedDict) → DI container uniquement — `get_app_config("testing")` en test, jamais de sous-classe
- `FlaskConfig` (classe) → Flask uniquement via `app.config.from_object()`
- `get_flask_config(app_config, config_name)` bridge les deux : copie `JWT_SECRET_KEY` dans FlaskConfig via `apply_jwt_config()`

See [config](.claude/commands/config.md).

### Authentication & JWT
- `@jwt_required()` goes immediately after the route decorator, before `@blp.arguments`
- `auth_controller.py` is the **only** controller allowed to use `try/except`
- Token creation (`create_access_token`) belongs in `auth_mapper.py`, never in the service

See [jwt-authentication](.claude/commands/jwt-authentication.md) and [jwt_security.md](docs/jwt_security.md).

### Error Handling
- Controllers must **not** wrap endpoint logic in `try/except` (except `auth_controller.py`)
- Controllers must **not** log the incoming request — `request_logger.py` does it globally

See [error-handling](.claude/commands/error-handling.md).

### Models
- Use `StrEnum` for status/type enums — never `str, Enum` (Python 3.11+ breaks serialization)

### Dependency Injection
- ISP: one ABC per operation in `repositories/`, one service class per operation in `services/`
- Controllers are auto-wired via `pkgutil.walk_packages` — never list them manually

See [dependency-injection](.claude/commands/dependency-injection.md).

### CI/CD
Quality checks run automatically on every push/PR — see [CI/CD Workflow Guide](.claude/commands/python-pep8-conventions-references/ci-cd-workflow.md).
