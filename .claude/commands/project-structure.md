# Project Structure

**Architecture Pattern**: 5-layer MVC with Flask
- See data flow examples in [architecture.md](../../docs/architecture.md)

```
source/
├── app.py                   (entry point — init logger, run server)
├── create_app.py            (Flask app factory — also owns the jwt = JWTManager() singleton)
├── container.py             (dependency injection container)
├── config/
│   ├── __init__.py          ← empty, package marker only
│   ├── app_config.py        (AppConfig TypedDict, get_app_config())
│   └── flask_config.py      (FlaskConfig + subclasses, API_SPEC_OPTIONS for Swagger JWT)
├── models/
│   ├── __init__.py
│   ├── task.py              (TaskStatus enum, TaskData, TaskUpdateData, Task)
│   ├── greeting.py          (Greeting)
│   ├── user.py              (UserData dataclass, User dataclass)
│   ├── not_found_error.py   (NotFoundError — raised by repositories when id not found)
│   ├── invalid_credentials_error.py  (InvalidCredentialsError — bad username or password)
│   └── user_already_exists_error.py  (UserAlreadyExistsError — duplicate username on register)
├── repositories/
│   ├── __init__.py
│   ├── create_task_repository.py        (CreateTaskRepository ABC)
│   ├── get_all_tasks_repository.py      (GetAllTasksRepository ABC)
│   ├── get_task_repository.py           (GetTaskRepository ABC)
│   ├── update_task_repository.py        (UpdateTaskRepository ABC)
│   ├── delete_task_repository.py        (DeleteTaskRepository ABC)
│   ├── fake_task_repository.py          (in-memory implementation of all task ABCs)
│   ├── register_user_repository.py      (RegisterUserRepository ABC)
│   ├── get_user_by_username_repository.py (GetUserByUsernameRepository ABC)
│   └── fake_user_repository.py          (in-memory implementation of all user ABCs)
├── services/
│   ├── __init__.py
│   ├── greeting_service.py         (GreetingService)
│   ├── create_task_service.py      (CreateTaskService)
│   ├── get_all_tasks_service.py    (GetAllTasksService)
│   ├── get_task_service.py         (GetTaskService)
│   ├── update_task_service.py      (UpdateTaskService)
│   ├── delete_task_service.py      (DeleteTaskService)
│   ├── register_user_service.py    (RegisterUserService — hashes password, delegates to repo)
│   └── login_user_service.py       (LoginUserService — verifies password, raises InvalidCredentialsError)
├── controllers/
│   ├── __init__.py
│   ├── greeting_controller.py
│   ├── tasks_controller.py  (POST, GET list, GET /{id}, PUT /{id}, DELETE /{id} — all @jwt_required)
│   ├── auth_controller.py   (POST /auth/register, POST /auth/login)
│   ├── schemas/              ← one file per schema
│   │   ├── __init__.py
│   │   ├── link_schema.py             (LinkSchema, LinksSchema — HATEOAS)
│   │   ├── task_data_schema.py        (TaskDataSchema — POST body)
│   │   ├── task_update_data_schema.py (TaskUpdateDataSchema — PUT body)
│   │   ├── task_schema.py             (TaskSchema — response)
│   │   ├── auth_data_schema.py        (AuthDataSchema — login/register body)
│   │   ├── user_schema.py             (UserSchema — register response)
│   │   └── token_schema.py            (TokenSchema — login response)
│   ├── entities/             ← one file per controller output DTO
│   │   ├── __init__.py
│   │   ├── link.py           (HttpMethod enum, LinkEntity, LinksEntity)
│   │   ├── greeting_entity.py
│   │   ├── task_entity.py    (TaskDataEntity, TaskUpdateDataEntity, TaskLinks, TaskEntity)
│   │   └── auth_entity.py    (AuthDataEntity, UserLinksEntity, UserEntity, TokenLinksEntity, TokenEntity)
│   ├── mappers/              ← one file per resource
│   │   ├── __init__.py
│   │   ├── greeting_mapper.py
│   │   ├── task_mapper.py    (to_task_data, to_task_update_data, to_task_entity)
│   │   └── auth_mapper.py    (to_auth_data, to_user_entity, to_token_entity — calls create_access_token)
│   └── utils/
│       ├── error_handlers.py (centralized Flask error handler)
│       ├── request_logger.py (before_request logger)
│       └── jwt_errors.py     (JWT-specific error callbacks: expired → 401, invalid → 422)
└── tests/
    ├── __init__.py
    ├── unit/
    │   ├── test_models/
    │   ├── test_services/
    │   ├── test_controllers/
    │   ├── test_repositories/
    │   └── test_utils/
    └── integration/
        ├── test_greeting_controller.py
        ├── test_tasks_controller.py
        └── test_auth_controller.py
```
