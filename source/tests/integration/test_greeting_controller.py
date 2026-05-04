import pytest
from source.create_app import create_app
from source.config.app_config import get_app_config
from source.config.flask_config import TestingFlaskConfig


@pytest.fixture
def app():
    application = create_app(TestingFlaskConfig(), get_app_config("testing"))
    application.config["TESTING"] = True
    return application


@pytest.fixture
def client(app):
    return app.test_client()


def test_get_greeting_returns_200(client):
    response = client.get("/v1/hello")
    assert response.status_code == 200


def test_get_greeting_returns_json(client):
    response = client.get("/v1/hello")
    data = response.get_json()
    assert data is not None
    assert "id" in data
    assert "message" in data


def test_get_greeting_message_content(client):
    response = client.get("/v1/hello")
    data = response.get_json()
    assert data["message"] == "Hello from API!"
    assert data["id"] == 1
