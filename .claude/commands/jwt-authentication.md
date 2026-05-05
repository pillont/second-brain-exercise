# Authentication & JWT Convention

The API uses **flask-jwt-extended** for stateless JWT authentication. Routes that require a logged-in user are decorated with `@jwt_required()`.

## Config architecture

Two config classes coexist, each with a single responsibility:

| Class | File | Passed to | Purpose |
|---|---|---|---|
| `FlaskConfig` | `flask_config.py` | `app.config.from_object()` | Flask/OpenAPI settings |
| `AppConfig` | `app_config.py` | DI container via `setup_container()` | Application settings (JWT secret, log level) |

`AppConfig` is a `TypedDict`:

```python
class AppConfig(TypedDict):
    LOG_LEVEL: int
    JWT_SECRET_KEY: str
```

`get_app_config(config_name)` uses a `match` statement to return the right dict. In tests always call `get_app_config("testing")` — **never** create a `TestingAppConfig` class.

`get_flask_config(app_config, config_name)` takes `AppConfig` as its first argument — it calls `apply_jwt_config()` internally to copy `JWT_SECRET_KEY` and `JWT_ACCESS_TOKEN_EXPIRES` from `AppConfig` into the `FlaskConfig` instance before returning it:

```python
def get_flask_config(app_config: AppConfig, config_name: str = "development") -> FlaskConfig:
    config = _flask_configs.get(config_name, DevelopmentFlaskConfig())
    apply_jwt_config(config, app_config)
    return config

def apply_jwt_config(config: FlaskConfig, app_config: AppConfig) -> None:
    config.JWT_SECRET_KEY = app_config["JWT_SECRET_KEY"]
    config.JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
```

Entry point in `app.py`:
```python
app_config = get_app_config()
app = create_app(get_flask_config(app_config), app_config)
```

## Flask config keys

`FlaskConfig` must declare:

| Key | Value | Purpose |
|---|---|---|
| `JWT_SECRET_KEY` | set from `AppConfig` via `apply_jwt_config()` | signing key for tokens |
| `JWT_ACCESS_TOKEN_EXPIRES` | `timedelta(minutes=15)` | token lifetime |
| `API_SPEC_OPTIONS` | see below | Authorize button in Swagger UI |

The `API_SPEC_OPTIONS` dict wires the Swagger UI Authorize button — **do not use the non-existent `OPENAPI_SECURITY_SCHEMES` / `OPENAPI_SECURITY` keys**:

```python
API_SPEC_OPTIONS = {
    "components": {
        "securitySchemes": {
            "BearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT",
            }
        }
    },
    "security": [{"BearerAuth": []}],
}
```

## Initialization

`jwt = JWTManager()` is declared as a module-level singleton in `create_app.py` and initialized with `jwt.init_app(app)` inside `_init_app()`:

```python
from flask_jwt_extended import JWTManager
jwt = JWTManager()

def _init_app(flask_config: FlaskConfig, app_config: AppConfig) -> FlaskApp:
    app = FlaskApp(__name__)
    app.config.from_object(flask_config)
    app.container = setup_container(app_config)
    jwt.init_app(app)
    return app
```

## DI container and AppConfig

The container receives the full `AppConfig` dict via `from_dict`. Services that need config values receive `config.provided` (the resolved dict proxy):

```python
class Container(containers.DeclarativeContainer):
    config = Configuration()
    login_user_service = Singleton(
        LoginUserService,
        repository=user_repository,
        config=config.provided,
    )

def setup_container(app_config: AppConfig) -> Container:
    container = Container()
    container.config.from_dict(cast(dict, app_config))
    ...
```

`LoginUserService.__init__` is typed `config: AppConfig` and accesses values via dict syntax: `self._config["JWT_SECRET_KEY"]`.

## JWT error callbacks

`source/controllers/utils/jwt_errors.py` registers two callbacks on the `jwt` singleton:

| Callback | Trigger | HTTP status |
|---|---|---|
| `@jwt.expired_token_loader` | expired token | 401 |
| `@jwt.invalid_token_loader` | malformed / missing token | 422 |

## Protecting a route

Place `@jwt_required()` immediately after the route decorator and before `@blp.arguments` / `@blp.response`:

```python
@tasks_blp.route("/", methods=["POST"])
@jwt_required()
@tasks_blp.arguments(TaskDataSchema)
@tasks_blp.response(201, TaskSchema)
@inject
def create_task(task_data_dto, create_task_service=Provide[...]) -> TaskDTO:
    ...
```

Unauthenticated requests to a protected route receive **401**.

## Auth endpoints

| Endpoint | Method | Description | Success | Error |
|---|---|---|---|---|
| `/auth/register` | POST | Create a new user | 201 `UserDTO` | 409 duplicate username, 422 bad body |
| `/auth/login` | POST | Authenticate and get a token | 200 `TokenDTO` | 401 wrong credentials, 422 bad body |

`auth_controller.py` is the **only** controller that uses `try/except` — it catches domain errors and converts them to HTTP errors via `abort()`:

```python
@auth_blp.route("/register", methods=["POST"])
@auth_blp.arguments(AuthDataSchema)
@auth_blp.response(409)
@auth_blp.response(201, UserSchema)
@inject
def register(auth_data_dto, register_user_service=Provide[...]) -> UserDTO:
    user_data = to_auth_data(auth_data_dto)
    try:
        user = register_user_service.register_user(user_data)
    except UserAlreadyExistsError:
        abort(409)
    return to_user_dto(user)

@auth_blp.route("/login", methods=["POST"])
@auth_blp.arguments(AuthDataSchema)
@auth_blp.response(401)
@auth_blp.response(200, TokenSchema)
@inject
def login(auth_data_dto, login_user_service=Provide[...]) -> TokenDTO:
    try:
        user = login_user_service.login(
            auth_data_dto["username"],
            auth_data_dto["password"],
        )
        return to_token_dto(user)
    except InvalidCredentialsError:
        abort(401)
```

## User models

```python
@dataclass
class UserData:
    username: str
    password: str          # plain text — input only, never stored

@dataclass
class HashedUserData:
    username: str
    hashed_password: str   # passed from service to repository after hashing

@dataclass
class User:
    id: int
    username: str
    hashed_password: str   # stored value
```

## Password hashing

Hashing belongs in `RegisterUserService`, not in the repository or controller. The service builds a `HashedUserData` before calling the repository:

```python
from werkzeug.security import generate_password_hash

def register_user(self, user_data: UserData) -> User:
    hashed = HashedUserData(
        username=user_data.username,
        hashed_password=generate_password_hash(user_data.password),
    )
    return self._repository.register(hashed)
```

`RegisterUserRepository.register()` accepts `HashedUserData`, never plain `UserData`.

Verification belongs in `LoginUserService`:

```python
from werkzeug.security import check_password_hash

def _validate_password_or_throw(self, user: User, password: str) -> None:
    if not check_password_hash(user.hashed_password, password):
        raise InvalidCredentialsError()
```

## LoginUserService returns User, not a token

`LoginUserService.login()` validates credentials and returns the `User` domain object. It does **not** generate a JWT:

```python
def login(self, username: str, password: str) -> User:
    user = self._get_user(username)
    self._validate_password_or_throw(user, password)
    return user
```

## Token creation

Token creation belongs in `auth_mapper.py` — **never in the controller or service**:

```python
from flask_jwt_extended import create_access_token

def to_token_dto(user: User) -> TokenDTO:
    token = create_access_token(str(user.id))   # subject = user id as string
    return TokenDTO(token=token, links=_build_token_links())
```

## Input validation

`AuthDataSchema` enforces a minimum password length of 8 characters:

```python
password = fields.Str(required=True, load_only=True, validate=validate.Length(min=8))
```

## Integration test fixtures for JWT

Protected routes require a valid token. Define these fixtures once per integration test file:

```python
from source.config.app_config import get_app_config
from source.config.flask_config import TestingFlaskConfig
from source.create_app import create_app

@pytest.fixture
def app():
    application = create_app(TestingFlaskConfig(), get_app_config("testing"))
    application.config["TESTING"] = True
    return application

USER_CREDENTIALS = {"username": "taskuser", "password": "taskpass1"}

@pytest.fixture
def token(app):
    with app.test_client() as c:
        c.post("/auth/register", json=USER_CREDENTIALS)
        resp = c.post("/auth/login", json=USER_CREDENTIALS)
        return resp.get_json()["token"]

@pytest.fixture
def client(app, token):
    c = app.test_client()
    c.environ_base["HTTP_AUTHORIZATION"] = f"Bearer {token}"
    return c
```

For tests that verify **unauthenticated access is rejected**:

```python
@pytest.fixture
def unauthenticated_client(app):
    return app.test_client()

def test_get_tasks_without_auth_returns_401(unauthenticated_client) -> None:
    response = unauthenticated_client.get("/tasks/")
    assert response.status_code == 401
```

For service-error tests that create an inner `app.test_client()`, set `environ_base` on that client too:

```python
def test_post_task_service_error_returns_500(app, token) -> None:
    mock_service = MagicMock()
    mock_service.create_task.side_effect = RuntimeError("Service failure")
    with app.test_client() as client:
        client.environ_base["HTTP_AUTHORIZATION"] = f"Bearer {token}"
        with app.container.create_task_service.override(mock_service):
            response = client.post("/tasks/", json=VALID_BODY)
        assert response.status_code == 500
```
