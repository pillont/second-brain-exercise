# HATEOAS & Controller Entities Pattern

All API responses follow HATEOAS — each response includes a `_links` object with hypermedia links describing available actions and the current resource.

## Separation of concerns

**Domain models** (`source/models/`) are pure and never carry hypermedia links.

**Controller entities** (`source/controllers/entities/`) are output DTOs specific to the controller layer. They wrap the domain model data and add the `_links` field before serialization.

**Mappers** (`source/controllers/mappers/`) handle the conversion between domain models and controller entities. Controllers delegate all mapping to them.

## File structure

| File | Purpose |
|---|---|
| `source/controllers/entities/link.py` | `Link` and `Links` dataclasses (shared by all controllers) |
| `source/controllers/entities/<resource>_entity.py` | DTO for a given resource |
| `source/controllers/schemas/link_schema.py` | `LinkSchema` and `LinksSchema` (shared by all schemas) |
| `source/controllers/schemas/<resource>_schema.py` | Schema for the entity, includes `_links` field |
| `source/controllers/mappers/<resource>_mapper.py` | `to_<resource>_entity()` and input mapping functions |

## `data_key` mapping convention

| Python attribute | JSON key | Reason |
|---|---|---|
| `self_link` | `"self"` | `self` is a Python naming convention — not a keyword but confusing |
| `links` | `"_links"` | HATEOAS standard prefix |

## Full example

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

**mappers/greeting_mapper.py**:
```python
from source.controllers.entities.link import LinkEntity
from source.controllers.entities.greeting_entity import GreetingEntity, GreetingLinks
from source.models.greeting import Greeting

def _build_links() -> GreetingLinks:
    return GreetingLinks(self_link=LinkEntity(href="/hello"))

def to_greeting_entity(greeting: Greeting) -> GreetingEntity:
    return GreetingEntity(id=greeting.id, message=greeting.message, links=_build_links())
```

**greeting_controller.py**:
```python
greeting_blp = Blueprint(
    "greeting",
    __name__,
    url_prefix="",
    description="Greeting endpoints.",
)

@greeting_blp.route("/hello", methods=["GET"])
@greeting_blp.doc(summary="Greeting", description="Returns a greeting message.")
@greeting_blp.response(200, GreetingSchema)
@inject
def get_greeting(greeting_service=Provide[Container.greeting_service]) -> GreetingEntity:
    return to_greeting_entity(greeting_service.get_greeting())
```

## TypedDict constructor — never use `cast()`

Always use the constructor with keyword arguments:

```python
return TaskLinks(
    self_link=LinkEntity(href=f"/tasks/{task.id}"),
    tasks=LinkEntity(href="/tasks/"),
    update=LinkEntity(href=f"/tasks/{task.id}", type=HttpMethod.PUT),
    delete=LinkEntity(href=f"/tasks/{task.id}", type=HttpMethod.DELETE),
)
```

Never use dict literal + `cast()` — it bypasses type checking:

```python
return cast(TaskLinks, {"self_link": {"href": "..."}})
```

## Task links reference

| Key | Method | href | Purpose |
|---|---|---|---|
| `self` | — | `/tasks/{id}` | The task itself |
| `tasks` | — | `/tasks/` | The task collection |
| `update` | `PUT` | `/tasks/{id}` | Update the task |
| `delete` | `DELETE` | `/tasks/{id}` | Delete the task |

## Rules

- Never add `links` to a domain model — models stay pure
- Never build links in a service or controller — link building belongs in the mapper
- Never write mapping logic inline in a controller — delegate to `<resource>_mapper.py`
- Reuse `link.py` and `link_schema.py` — do not create new `LinkEntity`/`LinksEntity` classes per resource
- One entity file per resource — naming: `<resource>_entity.py` → `class <Resource>Entity`
- One mapper file per resource — naming: `<resource>_mapper.py`
- Never use `cast()` — use the TypedDict constructor with kwargs instead
