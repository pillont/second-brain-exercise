# Serialization Pattern (flask-smorest + marshmallow)

Controllers **never** call `schema.dump()` manually. Use the `@blp.response` decorator so flask-smorest serializes the return value automatically:

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

## Rules

- **One schema per file** in `source/controllers/schemas/` — naming: `<resource>_schema.py` → `class <Resource>Schema(Schema)`
- No need to instantiate the schema class (flask-smorest handles it)
- Register blueprints via `api.register_blueprint()` (not `app.register_blueprint()`), where `api = Api(app)` in `create_app()`
- The `Config` base class must include `API_TITLE`, `API_VERSION`, and `OPENAPI_VERSION` for flask-smorest
- flask-smorest exposes `/openapi.json` and `/swagger-ui` automatically
- **No `# type: ignore`** — third-party packages without stubs are configured in `mypy.ini` with `ignore_missing_imports = True` per package section
