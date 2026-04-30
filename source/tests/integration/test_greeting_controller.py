from unittest.mock import MagicMock

import pytest
from source.create_app import create_app
from source.config.app_config import TestingAppConfig
from source.config.flask_config import TestingFlaskConfig


@pytest.fixture
def app():
    application = create_app(TestingFlaskConfig(), TestingAppConfig())
    application.config["TESTING"] = True
    return application


@pytest.fixture
def client(app):
    return app.test_client()


def test_get_greeting_returns_200(client):
    response = client.get("/hello")
    assert response.status_code == 200


def test_get_greeting_returns_json(client):
    response = client.get("/hello")
    data = response.get_json()
    assert data is not None
    assert "id" in data
    assert "message" in data


def test_get_greeting_message_content(client):
    response = client.get("/hello")
    data = response.get_json()
    assert data["message"] == "Hello from API!"
    assert data["id"] == 1


def test_get_greeting_service_error(app):
    with app.test_client() as client:
        mock_service = MagicMock()
        mock_service.get_greeting.side_effect = RuntimeError("Service failure")
        with app.container.greeting_service.override(mock_service):
            response = client.get("/hello")
        assert response.status_code == 500
        data = response.get_json()
        assert "error" in data
