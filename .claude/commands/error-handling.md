# Error Handling & Request Logging Convention

**Controllers must NOT wrap endpoint logic in try/except** (sole exception: `auth_controller.py`).

Two cross-cutting hooks are registered in `source/controllers/utils/` and wired in `create_app()`:

| File | Hook | Purpose |
|---|---|---|
| `error_handlers.py` | `@app.errorhandler(Exception)` | Catches all unhandled exceptions, logs at ERROR, returns HTTP 500 |
| `request_logger.py` | `@app.before_request` | Logs `METHOD /path` for every incoming request |

Because `request_logger.py` handles request logging globally, **controllers must not log the incoming request themselves**.

## Correct controller pattern

```python
@blueprint.route("/example", methods=["GET"])
@inject
def get_example(my_service=Provide[Container.my_service]) -> MyEntity:
    result = my_service.do_something()
    return to_my_entity(result)
```

Services and repositories may still raise domain-specific exceptions — the global handler catches anything that bubbles up uncaught.
