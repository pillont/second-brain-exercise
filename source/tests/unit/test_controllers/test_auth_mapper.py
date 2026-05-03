import pytest
from source.config.app_config import get_app_config
from source.config.flask_config import TestingFlaskConfig
from source.controllers.entities.auth_entity import AuthDataEntity
from source.controllers.entities.link import HttpMethod
from source.controllers.mappers.auth_mapper import (
    to_auth_data,
    to_token_entity,
    to_user_entity,
)
from source.create_app import create_app
from source.models.user import User, UserData


@pytest.fixture
def app():
    application = create_app(TestingFlaskConfig(), get_app_config("testing"))
    application.config["TESTING"] = True
    return application


def _make_user() -> User:
    return User(id=1, username="alice", hashed_password="hashed")


def test_to_auth_data_maps_fields() -> None:
    entity = AuthDataEntity(username="alice", password="secret")

    result = to_auth_data(entity)

    assert isinstance(result, UserData)
    assert result.username == "alice"
    assert result.password == "secret"


def test_to_user_entity_maps_fields() -> None:
    result = to_user_entity(_make_user())

    assert result["id"] == 1
    assert result["username"] == "alice"


def test_to_user_entity_sets_self_link() -> None:
    result = to_user_entity(_make_user())

    assert result["links"]["self_link"]["href"] == "/auth/register"


def test_to_user_entity_sets_login_link() -> None:
    result = to_user_entity(_make_user())

    assert result["links"]["login"]["href"] == "/auth/login"
    assert result["links"]["login"]["type"] == HttpMethod.POST


def test_to_token_entity_maps_token(app) -> None:
    with app.app_context():
        result = to_token_entity(_make_user())

    assert isinstance(result["token"], str)
    assert len(result["token"]) > 0


def test_to_token_entity_sets_self_link(app) -> None:
    with app.app_context():
        result = to_token_entity(_make_user())

    assert result["links"]["self_link"]["href"] == "/auth/login"


def test_to_token_entity_sets_register_link(app) -> None:
    with app.app_context():
        result = to_token_entity(_make_user())

    assert result["links"]["register"]["href"] == "/auth/register"
    assert result["links"]["register"]["type"] == HttpMethod.POST


def test_to_token_entity_sets_get_all_tasks_link(app) -> None:
    with app.app_context():
        result = to_token_entity(_make_user())

    assert result["links"]["get_all_tasks"]["href"] == "/tasks/"
    assert "type" not in result["links"]["get_all_tasks"]


def test_to_token_entity_sets_create_task_link(app) -> None:
    with app.app_context():
        result = to_token_entity(_make_user())

    assert result["links"]["create_task"]["href"] == "/tasks/"
    assert result["links"]["create_task"]["type"] == HttpMethod.POST
