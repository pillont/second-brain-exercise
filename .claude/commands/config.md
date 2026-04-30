# Configuration Architecture

The config layer is split into two classes with responsibilities distinctes.

## Deux classes, deux destinations

| Classe | Fichier | Passée à | Contenu |
|---|---|---|---|
| `FlaskConfig` | `source/config/flask_config.py` | `app.config.from_object()` | Paramètres Flask/OpenAPI/JWT |
| `AppConfig` | `source/config/app_config.py` | DI container via `setup_container()` | Paramètres applicatifs |

**Règle** : ne jamais passer `FlaskConfig` au container DI, ne jamais passer `AppConfig` à Flask.

## AppConfig — TypedDict

`AppConfig` est un `TypedDict`, pas une classe :

```python
class AppConfig(TypedDict):
    LOG_LEVEL: int
    JWT_SECRET_KEY: str
```

`get_app_config(config_name)` retourne le bon dict via un `match` :

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

Pour ajouter une nouvelle clé : l'ajouter dans `AppConfig` (TypedDict) **et** dans chaque `case` du `match`.

Ne jamais créer de sous-classe de `AppConfig` (ex: `TestingAppConfig`) — toujours utiliser `get_app_config("testing")`.

## FlaskConfig — hiérarchie de classes

`FlaskConfig` et ses variantes sont des classes standard Flask :

```
FlaskConfig
├── DevelopmentFlaskConfig   DEBUG = True
├── TestingFlaskConfig       TESTING = True
└── ProductionFlaskConfig    SECRET_KEY depuis env (obligatoire)
```

`get_flask_config(app_config, config_name)` prend `AppConfig` en premier argument — il appelle `apply_jwt_config()` pour copier les valeurs JWT dans le `FlaskConfig` avant de le retourner :

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

`JWT_SECRET_KEY` est ainsi la **source unique** : définie dans `AppConfig`, utilisée à la fois par Flask (pour signer les tokens via flask-jwt-extended) et par le container DI (pour `LoginUserService`).

## Flux complet

```
app.py
  ├── app_config = get_app_config()
  └── create_app(get_flask_config(app_config), app_config)
        ├── app.config.from_object(flask_config)   ← Flask reçoit FlaskConfig
        └── setup_container(app_config)            ← DI reçoit AppConfig
              └── container.config.from_dict(cast(dict, app_config))
```

## Container DI et AppConfig

Le container charge l'`AppConfig` via `from_dict`. Les services qui ont besoin de la config reçoivent `config.provided` (proxy résolu au moment de l'injection) :

```python
class Container(containers.DeclarativeContainer):
    config = Configuration()
    login_user_service = Singleton(
        LoginUserService,
        repository=user_repository,
        config=config.provided,   # injecte le dict AppConfig résolu
    )

def setup_container(app_config: AppConfig) -> Container:
    container = Container()
    container.config.from_dict(cast(dict, app_config))
    ...
```

Les services typent leur paramètre `config: AppConfig` et accèdent aux valeurs via la syntaxe dict : `self._config["JWT_SECRET_KEY"]`.

## En test

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
