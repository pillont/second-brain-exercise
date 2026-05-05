# Task Management API

A RESTful task management API built with Flask, implementing JWT authentication, HATEOAS, cursor-based pagination, and a clean 5-layer MVC architecture.

---

## Quick Start

### Prerequisites

- Python 3.14
- pip

### Install

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Run

**VS Code (recommended):** press **F5** — the server starts and Swagger UI opens automatically.

**Terminal:**

```bash
.venv/bin/python -m source.app
```

The API runs on **http://127.0.0.1:5001** (port 5001 — macOS AirPlay Receiver occupies 5000).

Swagger UI: **http://127.0.0.1:5001/swagger-ui**

### Test & Lint

```bash
# Tests
python -m pytest source/tests/ -v
python -m pytest source/tests/unit/ -v
python -m pytest source/tests/integration/ -v
python -m pytest source/tests/ --cov=source --cov-report=html

# Quality checks
python -m flake8 source/
python -m black source/
python -m mypy source/
python -m pylint source/ --disable=C0111
```

---

## Exercise

The original exercise brief: [EXERCISE.md](./EXERCISE.md)

---

## What Was Built

### Project Structure

5-layer MVC: `config → models → repositories → services → controllers`.

Each layer has a single responsibility — no business logic in controllers, no HTTP concepts in services.
See [project-structure](.claude/commands/project-structure.md) for the full file tree and layer responsibilities.

### Code Conventions

- PEP 8: snake_case, 88-char line limit, `black` formatting
- No comments or docstrings — code is self-documenting through naming
- 120-line max per file, 6-line max per function body
- Function names always start with a verb (`get_`, `apply_`, `build_`)
- Module-level pure functions over private class methods when `self` is not needed

See [conventions](.claude/commands/conventions.md).

### SOLID & Dependency Injection

ISP is applied at every layer: one interface (ABC) per operation in both `repositories/` and `services/` — e.g. `CreateTaskRepository`, `GetAllTasksRepository`, `UpdateTaskRepository`. No fat interfaces.

The DI container wires dependencies automatically. Controllers are registered via `pkgutil.walk_packages` — no manual listing. Each provider maps to exactly one interface, even for fakes.

See [dependency-injection](.claude/commands/dependency-injection.md).

### Type Safety

100% type-annotated codebase validated with MyPy. No `Any` — the most precise type is always used. `Final` is applied to every immutable `__init__` attribute across all classes.

### RESTful API + HATEOAS

Every response includes a `_links` object so clients can navigate the API without hardcoding URLs. Link construction is isolated in dedicated mapper files — never inline in controllers.

Swagger UI is auto-generated from code via `flask-smorest` — no YAML, no hand-written OpenAPI specs.

See [hateoas](.claude/commands/hateoas.md) and [serialization](.claude/commands/serialization.md).

### Testing (2 Levels)

**Unit tests** (`source/tests/unit/`) — services, repositories, models, and mappers tested in isolation using in-memory fakes.

**Integration tests** (`source/tests/integration/`) — full HTTP stack: real Flask app, fakes injected via the DI container, no mocks. Tests exercise the complete request/response cycle including serialization, JWT validation, and error handling.

See [testing-conventions](.claude/commands/testing-conventions.md).

### JWT Authentication

`@jwt_required()` protects all task endpoints. Passwords are hashed with `werkzeug`. Token creation is isolated in `auth_mapper.py` — services stay free of HTTP concerns.

See [jwt_security.md](docs/jwt_security.md) and [jwt-authentication](.claude/commands/jwt-authentication.md).

### Volume Management

#### Pagination & Filtering

`GET /v1/tasks` supports **cursor-based pagination** — more robust than offset-based: no duplicate rows when data is inserted or deleted between pages. Supports filtering by `status`, `title`, `due_date_from`, `due_date_to` and sorting by any field (`id`, `title`, `due_date`, `status`) in either direction.

Inspired by: [Pagination Demystified — Three Layers You Shouldn't Mix Up](https://medium.com/@tpierrain/pagination-demystified-three-layers-you-shouldnt-mix-up-b5cca3b8e755)

See [pagination.md](docs/pagination.md) for the cursor encoding strategy and filter implementation details.

#### Database Indexes

`title`, `due_date`, and `status` are indexed at the SQLAlchemy ORM level — filter and sort queries stay performant as the dataset grows, with no manual migration required.

### SQLAlchemy Integration

Repository pattern with one class per operation, each in its own file. The SQLAlchemy engine is declared as `providers.Singleton` in the DI container so all repositories share the same connection pool.

See [sqlalchemy-repositories](.claude/commands/sqlalchemy-repositories.md).

### CI/CD

Every push and PR runs: `flake8`, `black --check`, `mypy`, `pylint`, and `pytest` via GitHub Actions.

See [CI-CD.md](.github/CI-CD.md).

### Claude Integration (Vibe Coding)

This project is fully configured for AI-assisted development with [Claude Code](https://claude.ai/code).

**What's in place:**

- **[CLAUDE.md](./CLAUDE.md)** — project instructions loaded automatically into every Claude session: architecture rules, naming conventions, layer responsibilities, and coding standards
- **[.claude/commands/](.claude/commands/)** — skill files for each convention (HATEOAS, serialization, JWT, DI, error handling, testing…) referenced directly from CLAUDE.md and invocable as slash commands
- **[.claude/settings.json](.claude/settings.json)** — pre-authorized tools and permissions so Claude can run tests, linters, and the dev server without interruption
- **Memory system** — cross-session memory stores feedback, decisions, and project context so Claude maintains consistency across conversations

The result: Claude understands the full architecture, applies the conventions automatically, and can take a feature from model to integration test without guidance on structure or style.
