# Configuration Architecture

The config layer is split into two classes with distinct responsibilities.

## Two classes, two destinations

| Class | File | Passed to | Content |
|---|---|---|---|
| `FlaskConfig` | `source/config/flask_config.py` | `app.config.from_object()` | Flask/OpenAPI/JWT parameters |
| `AppConfig` | `source/config/app_config.py` | DI container via `setup_container()` | Application parameters |

**Rule**: never pass `FlaskConfig` to the DI container, never pass `AppConfig` to Flask.

## AppConfig — TypedDict

`AppConfig` is a `TypedDict`, not a class:

```python
class AppConfig(TypedDict):
    LOG_LEVEL: int
    JWT_SECRET_KEY: str
```

`get_app_config(config_name)` returns the right dict via a `match`:

```python
def get_app_config(config_name: str = "development") -> AppConfig:
    match config_name:
        case "development":
            return {"LOG_LEVEL": logging.DEBUG, "JWT_SECRET_KEY": JWT_SECRET_KEY}
        case "testing":
            return {"LOG_LEVEL": logging.WARNING, "JWT_SECRET_KEY": "test-jwt-secret"}
        case "production":
            return {"LOG_LEVEL": logging.INFO, "JWT_SECRET_KEY": JWT_SECRET_KEY}
        case _:
            raise NotImplementedError()
```

To add a new key: add it to `AppConfig` (TypedDict) **and** to each `case` in the `match`.

Never subclass `AppConfig` (e.g. `TestingAppConfig`) — always use `get_app_config("testing")`.

## FlaskConfig — class hierarchy

`FlaskConfig` and its variants are standard Flask classes:

```
FlaskConfig
├── DevelopmentFlaskConfig   DEBUG = True
├── TestingFlaskConfig       TESTING = True
└── ProductionFlaskConfig    SECRET_KEY from env (required)
```

`get_flask_config(app_config, config_name)` takes `AppConfig` as its first argument — it calls `apply_jwt_config()` to copy JWT values into the `FlaskConfig` before returning it:

```python
def get_flask_config(
    app_config: AppConfig, config_name: str = "development"
) -> FlaskConfig:
    config = _flask_configs.get(config_name, DevelopmentFlaskConfig())
    apply_jwt_config(config, app_config)
    return config

def apply_jwt_config(config: FlaskConfig, app_config: AppConfig) -> None:
    config.JWT_SECRET_KEY = app_config["JWT_SECRET_KEY"]
    config.JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
```

`JWT_SECRET_KEY` is the **single source of truth**: defined in `AppConfig`, used by both Flask (to sign tokens via flask-jwt-extended) and the DI container (for `LoginUserService`).

## Full flow

```
app.py
  ├── app_config = get_app_config()
  └── create_app(get_flask_config(app_config), app_config)
        ├── app.config.from_object(flask_config)   ← Flask receives FlaskConfig
        └── setup_container(app_config)            ← DI receives AppConfig
              └── container.config.from_dict(cast(dict, app_config))
```

## DI container and AppConfig

The container loads `AppConfig` via `from_dict`. Services that need config values receive `config.provided` (the resolved dict proxy at injection time):

```python
class Container(containers.DeclarativeContainer):
    config = Configuration()
    login_user_service = Singleton(
        LoginUserService,
        repository=user_repository,
        config=config.provided,   # injects the resolved AppConfig dict
    )

def setup_container(app_config: AppConfig) -> Container:
    container = Container()
    container.config.from_dict(cast(dict, app_config))
    ...
```

Services type their `config` parameter as `AppConfig` and access values via dict syntax: `self._config["JWT_SECRET_KEY"]`.

## In tests

```python
from source.config.app_config import get_app_config
from source.config.flask_config import TestingFlaskConfig
from source.create_app import create_app

@pytest.fixture
def app():
    application = create_app(TestingFlaskConfig(), get_app_config("testing"))
    application.config["TESTING"] = True
    return application
```
