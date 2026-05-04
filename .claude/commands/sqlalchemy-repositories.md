# SQLAlchemy Repository Pattern

## Folder structure

```
repositories/
├── __init__.py                        ← ABCs only, no implementations
├── fake/
│   ├── __init__.py
│   ├── tasks_fake_repository.py       ← implements all 5 task ABCs
│   ├── tasks_list_filter.py           ← filter logic on Python lists
│   └── users_fake_repository.py
└── sqlalchemy/
    ├── session_utils.py               ← OrmSession + initialize_schema
    └── tasks/
        ├── task_orm_model.py          ← Base + TaskOrmModel
        └── repositories/
            ├── __init__.py            ← barrel for the 4 simple repos
            ├── create/
            │   ├── create_task_sqlalchemy_repository.py
            │   └── task_sqlalchemy_mapper.py
            ├── get_all/
            │   ├── __init__.py
            │   ├── get_all_tasks_sqlalchemy_repository.py
            │   ├── task_cursor.py          ← cursor/keyset pagination
            │   ├── tasks_sorter.py         ← ORDER BY logic
            │   └── tasks_statement_filter.py  ← WHERE clause logic
            ├── get_task_sqlalchemy_repository.py
            ├── update_task_sqlalchemy_repository.py
            └── delete_task_sqlalchemy_repository.py
```

## OrmSession

`session_utils.py` exposes a generic `OrmSession(Generic[T])` that wraps `engine + model_class`. Every repo stores one as `self._orm_session` — never manipulates sessions directly.

```python
class OrmSession(Generic[T]):
    def __init__(self, engine: Engine, model_class: type[T]) -> None: ...

    def add(self, orm_object: Base) -> None: ...          # INSERT + refresh (gets auto-increment id)
    def get_or_raise(self, entity_id: int) -> T: ...      # SELECT by PK, raises NotFoundError
    def select(self, select_statement: Select) -> List[T]: ...  # execute arbitrary SELECT
    def update_or_raise(self, entity_id: int, apply_update: Callable[[T], None]) -> None: ...
    def delete_or_raise(self, entity_id: int) -> None: ...
```

Each repo's `__init__` follows this exact pattern:

```python
def __init__(self, engine: Engine) -> None:
    self._orm_session: Final = OrmSession(initialize_schema(engine), TaskOrmModel)
```

`initialize_schema(engine)` calls `Base.metadata.create_all(engine)` and returns the engine.

## Simple repos (create, get, update, delete)

Each is a single file, one class, delegates entirely to `OrmSession`:

```python
# get
def get_task(self, id: int) -> Task:
    return to_task(self._orm_session.get_or_raise(id))

# update — lambda closes over task_update_data
def update(self, id: int, task_update_data: TaskUpdateData) -> None:
    self._orm_session.update_or_raise(
        id, lambda orm_task: _apply_update(orm_task, task_update_data)
    )

# delete
def delete_task(self, id: int) -> None:
    self._orm_session.delete_or_raise(id)
```

## get_all — split into 4 modules

| File | Responsibility |
|---|---|
| `get_all_tasks_sqlalchemy_repository.py` | Orchestration: build query → execute → map → paginate |
| `tasks_statement_filter.py` | `apply_tasks_filters(stmt, filters)` — WHERE clauses |
| `tasks_sorter.py` | `apply_sort(stmt, sort)` — ORDER BY |
| `task_cursor.py` | `apply_cursor(stmt, sort, cursor_row)` — keyset pagination |

### Keyset cursor pagination

Cursor is an entity `id`. `get_cursor_row` fetches the row, then SQL builds a WHERE that skips everything before it:

- ID sort: `WHERE id > cursor_id`
- Other field (e.g. title ASC): `WHERE (LOWER(title) > val) OR (LOWER(title) = val AND id > cursor_id)`

If the cursor id is not found, `NotFoundError` is raised (not a silent full-list fallback).

## ORM model

```python
class TaskOrmModel(Base):
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), index=True)
    description: Mapped[str] = mapped_column(Text)
    due_date: Mapped[date] = mapped_column(Date, index=True)
    status: Mapped[str] = mapped_column(String(50), index=True)
```

`status` is stored as `str` — the StrEnum value (e.g. `"Incomplete"`). The mapper converts to/from `TaskStatus`.

## Mapper (create/)

`task_sqlalchemy_mapper.py` holds both directions and is shared by `get_task` and `get_all` repos:

```python
def to_orm_task(task_data: TaskData) -> TaskOrmModel: ...   # domain → ORM (status = INCOMPLETE)
def to_task(orm_task: TaskOrmModel) -> Task: ...            # ORM → domain
```

## Unit tests for SQLAlchemy repos

Use `sqlite:///:memory:` with a single shared engine per test (via the `engine` fixture). All repos that share the same engine see the same in-memory database:

```python
@pytest.fixture
def engine(tmp_path) -> Engine:
    return create_engine("sqlite:///:memory:")
```
