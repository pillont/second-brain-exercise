# Coding Conventions

## Inheritance for variants

When creating an Update variant of a model/entity/schema, inherit from the base and only add the extra field — never re-declare shared fields:

```python
class TaskUpdateData(TaskData):
    status: TaskStatus

class TaskUpdateDataEntity(TaskDataEntity):
    status: TaskStatus

class TaskUpdateDataSchema(TaskDataSchema):
    status = fields.Enum(TaskStatus, by_value=True, required=True)

    @post_load
    def make_entity(self, data: dict, **kwargs: object) -> TaskUpdateDataEntity:
        return TaskUpdateDataEntity(**data)
```

## Update operations

`update` methods return `None` at every layer — repository ABC, service, and route. Routes use `@blp.response(204)`. Never return the updated resource from a PUT.

## `fields.Enum` — always `by_value=True`

Marshmallow 4 loads enums **by name** by default (`INCOMPLETE`, `COMPLETE`). Always add `by_value=True` so the API accepts the human-readable values (`"Incomplete"`, `"Complete"`):

```python
status = fields.Enum(TaskStatus, by_value=True, required=False)
```

## Generic vs resource-specific schemas and entities

Generic components (pagination) stay minimal. Resource-specific fields go in a subclass:

- `ListArgumentSchema(Schema)` → `cursor`, `page_size` only
- `TasksListArgumentSchema(ListArgumentSchema)` → adds filter fields
- Same pattern for TypedDict entities: `ListArgumentEntity` → `TasksListArgumentEntity(ListArgumentEntity)`
- The resource controller uses the resource-specific subclass, never the generic directly

## Filter parameter ordering in signatures

Domain filters come before pagination parameters in every `get_all` signature (ABC, repository implementation, service):

```python
def get_all(
    self,
    filters: Optional[TaskFilters] = None,
    cursor: Optional[int] = None,
    page_size: Optional[int] = None,
) -> FilteredList[Task]: ...
```

## Pure functions & classes

If a method doesn't use `self`, extract it as a **module-level private function** (`_` prefix). The class method becomes a pure orchestrator that passes the needed values as explicit parameters.

## Filter logic belongs in the repository layer, not the model

`TaskFilters` is a pure `@dataclass` — a data container. It does **not** have an `apply()` method. Filter logic lives in the repository implementation:

- Fake: `repositories/fake/tasks_list_filter.py` → operates on Python lists
- SQLAlchemy: `repositories/sqlalchemy/tasks/repositories/get_all/tasks_statement_filter.py` → builds SQL `WHERE` clauses

```python
# model — pure data, no logic
@dataclass
class TaskFilters:
    status: Optional[TaskStatus] = None
    title: Optional[str] = None
    description: Optional[str] = None

# fake filter module
def filter_tasks_list(elements: Iterable[Task], filters: TaskFilters) -> Iterable[Task]:
    if filters.status:
        elements = _filter_by_status(elements, filters.status)
    return elements

# SQLAlchemy filter module
def apply_tasks_filters(select_statement: Select, filters: Optional[TaskFilters]) -> Select:
    if not filters:
        return select_statement
    if filters.status:
        select_statement = _filter_by_status(select_statement, filters.status)
    return select_statement
```