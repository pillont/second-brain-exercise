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

## Always-On Rules

- No comments `#` or docstrings `"""` in any `.py` file
- `Final` on every `self.x` that is never reassigned — in every class
- 120 lines max per `.py` file (excluding tests) — split before adding code
- 6 lines max per function body — extract sub-functions
- Method ordering: `__init__` → public → private (`_`)
- Function names must start with a verb (`get_`, `apply_`, `build_`)
- No `Any` — use the most precise type, a base class, TypeVar, or protocol
- Module-level logger: `logger = logging.getLogger(__name__)` after imports, never passed as parameter
- `@dataclass` for pure data only — if a class has a business method, use a regular class
- ISP: one ABC per operation in `repositories/` and `services/`; same rule at container level
- No `# pylint: disable` inline — fix root cause or configure the tool
- `StrEnum` for enums — never `str, Enum`
- A `match` statement generally deserves its own function — keep calling function as orchestrator
- Prefer descriptive names over abbreviations (`select_statement` not `stmt`)
- Context before values in parameters (`persist(engine, orm_object)` not reversed)

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

## Skills

| Skill | Covers |
|---|---|
| [project-structure](.claude/commands/project-structure.md) | Full annotated file tree |
| [conventions](.claude/commands/conventions.md) | Inheritance, update ops, filter ordering, pure functions |
| [hateoas](.claude/commands/hateoas.md) | `_links`, entities, mappers, schemas |
| [serialization](.claude/commands/serialization.md) | flask-smorest, `@blp.response`, Swagger decorators |
| [config](.claude/commands/config.md) | AppConfig TypedDict, FlaskConfig, bridge function |
| [jwt-authentication](.claude/commands/jwt-authentication.md) | `@jwt_required()`, decorator order, auth_mapper |
| [error-handling](.claude/commands/error-handling.md) | Global handler, request_logger, no try/except |
| [dependency-injection](.claude/commands/dependency-injection.md) | Container, providers, auto-wiring |
| [sqlalchemy-repositories](.claude/commands/sqlalchemy-repositories.md) | SQLAlchemy pattern, engine Singleton |
| [testing-conventions](.claude/commands/testing-conventions.md) | Filter checklist, unit + integration patterns |
| [python-clean-code-solid](.claude/commands/python-clean-code-solid.md) | SOLID, clean code |
| [python-typing](.claude/commands/python-typing.md) | Type hints, MyPy |
| [python-pep8-conventions](.claude/commands/python-pep8-conventions.md) | PEP 8, Black, Flake8 |

## Docs

- [docs/architecture.md](docs/architecture.md) — data flow diagrams
- [docs/jwt_security.md](docs/jwt_security.md) — JWT security audit
- [docs/pagination.md](docs/pagination.md) — cursor-based pagination strategy
