# Serialization Pattern (flask-smorest + marshmallow)

Controllers **never** call `schema.dump()` manually. Use the `@blp.response` decorator so flask-smorest serializes the return value automatically:

```python
from flask_smorest import Blueprint
from source.models.my_model import MyModel
from source.controllers.schemas.my_schema import MySchema

my_blp = Blueprint(
    "my_resource",
    __name__,
    url_prefix="/my-resource",
    description="My resource description.",
)

@my_blp.route("/", methods=["GET"])
@my_blp.doc(summary="Get resource", description="Retrieve the resource.")
@my_blp.response(200, MySchema)
@inject
def get_resource(my_service=Provide[Container.my_service]) -> MyModel:
    return my_service.do_something()
```

## Swagger documentation

Every endpoint **must** have a `@blp.doc(summary=..., description=...)` decorator. Every Blueprint **must** have a `description=` parameter. Never use docstrings — `@blp.doc()` is the only accepted mechanism.

**Decorator order** (top → bottom):
1. `@blp.route(...)` — always first
2. `@jwt_required()` — immediately after the route (if auth required)
3. `@blp.doc(summary=..., description=...)` — before arguments/response
4. `@blp.arguments(...)` / `@blp.response(...)` — closest to the function

Use multi-line format when the decorator exceeds 88 characters:

```python
@my_blp.doc(
    summary="List resources",
    description="Retrieve all resources with optional filters.",
)
```

## Rules

- **One schema per file** in `source/controllers/schemas/` — naming: `<resource>_schema.py` → `class <Resource>Schema(Schema)`
- No need to instantiate the schema class (flask-smorest handles it)
- Register blueprints via `api.register_blueprint()` (not `app.register_blueprint()`), where `api = Api(app)` in `create_app()`
- The `Config` base class must include `API_TITLE`, `API_VERSION`, and `OPENAPI_VERSION` for flask-smorest
- flask-smorest exposes `/openapi.json` and `/swagger-ui` automatically
- **No `# type: ignore`** — third-party packages without stubs are configured in `mypy.ini` with `ignore_missing_imports = True` per package section
