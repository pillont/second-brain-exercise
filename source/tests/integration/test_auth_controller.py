from unittest.mock import MagicMock

import pytest

from source.config.app_config import get_app_config
from source.config.flask_config import TestingFlaskConfig
from source.create_app import create_app


@pytest.fixture
def app():
    application = create_app(TestingFlaskConfig(), get_app_config("testing"))
    application.config["TESTING"] = True
    return application


@pytest.fixture
def client(app):
    return app.test_client()


VALID_CREDENTIALS = {"username": "testuser", "password": "testpassword"}


@pytest.fixture
def registered_client(client):
    client.post("/auth/register", json=VALID_CREDENTIALS)
    return client


def test_register_returns_201(client) -> None:
    response = client.post("/auth/register", json=VALID_CREDENTIALS)

    assert response.status_code == 201


def test_register_response_has_expected_keys(client) -> None:
    response = client.post("/auth/register", json=VALID_CREDENTIALS)
    data = response.get_json()

    assert "id" in data
    assert "username" in data
    assert "_links" in data


def test_register_returns_username_matching_input(client) -> None:
    response = client.post("/auth/register", json=VALID_CREDENTIALS)
    data = response.get_json()

    assert data["username"] == VALID_CREDENTIALS["username"]


def test_register_returns_self_link(client) -> None:
    response = client.post("/auth/register", json=VALID_CREDENTIALS)
    data = response.get_json()

    assert data["_links"]["self"]["href"] == "/auth/register"


def test_register_returns_login_link(client) -> None:
    response = client.post("/auth/register", json=VALID_CREDENTIALS)
    data = response.get_json()

    assert data["_links"]["login"]["href"] == "/auth/login"
    assert data["_links"]["login"]["type"] == "POST"


def test_register_missing_username_returns_422(client) -> None:
    response = client.post("/auth/register", json={"password": "testpassword"})

    assert response.status_code == 422


def test_register_missing_password_returns_422(client) -> None:
    response = client.post("/auth/register", json={"username": "testuser"})

    assert response.status_code == 422


def test_register_duplicate_username_returns_409(client) -> None:
    client.post("/auth/register", json=VALID_CREDENTIALS)
    response = client.post("/auth/register", json=VALID_CREDENTIALS)

    assert response.status_code == 409


def test_register_service_error_returns_500(app) -> None:
    mock_service = MagicMock()
    mock_service.register_user.side_effect = RuntimeError("Service failure")
    with app.test_client() as client:
        with app.container.register_user_service.override(mock_service):
            response = client.post("/auth/register", json=VALID_CREDENTIALS)
        assert response.status_code == 500
        data = response.get_json()
        assert "error" in data


def test_login_returns_200(registered_client) -> None:
    response = registered_client.post("/auth/login", json=VALID_CREDENTIALS)

    assert response.status_code == 200


def test_login_response_has_expected_keys(registered_client) -> None:
    response = registered_client.post("/auth/login", json=VALID_CREDENTIALS)
    data = response.get_json()

    assert "token" in data
    assert "_links" in data


def test_login_token_is_non_empty_string(registered_client) -> None:
    response = registered_client.post("/auth/login", json=VALID_CREDENTIALS)
    data = response.get_json()

    assert isinstance(data["token"], str)
    assert len(data["token"]) > 0


def test_login_returns_self_link(registered_client) -> None:
    response = registered_client.post("/auth/login", json=VALID_CREDENTIALS)
    data = response.get_json()

    assert data["_links"]["self"]["href"] == "/auth/login"


def test_login_returns_register_link(registered_client) -> None:
    response = registered_client.post("/auth/login", json=VALID_CREDENTIALS)
    data = response.get_json()

    assert data["_links"]["register"]["href"] == "/auth/register"
    assert data["_links"]["register"]["type"] == "POST"


def test_login_invalid_password_returns_401(registered_client) -> None:
    response = registered_client.post(
        "/auth/login",
        json={
            "username": VALID_CREDENTIALS["username"],
            "password": "wrong_password_invalid",
        },
    )

    assert response.status_code == 401


def test_login_unknown_username_returns_401(client) -> None:
    response = client.post(
        "/auth/login",
        json={"username": "unknown", "password": "whatever"},
    )

    assert response.status_code == 401


def test_login_missing_username_returns_422(client) -> None:
    response = client.post("/auth/login", json={"password": "testpassword"})

    assert response.status_code == 422


def test_login_missing_password_returns_422(client) -> None:
    response = client.post("/auth/login", json={"username": "testuser"})

    assert response.status_code == 422


def test_login_service_error_returns_500(app) -> None:
    mock_service = MagicMock()
    mock_service.login.side_effect = RuntimeError("Service failure")
    with app.test_client() as client:
        client.post("/auth/register", json=VALID_CREDENTIALS)
        with app.container.login_user_service.override(mock_service):
            response = client.post("/auth/login", json=VALID_CREDENTIALS)
        assert response.status_code == 500
        data = response.get_json()
        assert "error" in data
