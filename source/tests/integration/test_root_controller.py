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


def test_get_entry_point_returns_200(client):
    response = client.get("/")
    assert response.status_code == 200


def test_get_entry_point_returns_links(client):
    data = client.get("/").get_json()
    assert data is not None
    assert "_links" in data


def test_get_entry_point_self_link(client):
    links = client.get("/").get_json()["_links"]
    assert links["self"] == {"href": "/v1/"}


def test_get_entry_point_register_link(client):
    links = client.get("/").get_json()["_links"]
    assert links["register"] == {"href": "/v1/auth/register", "type": "POST"}


def test_get_entry_point_login_link(client):
    links = client.get("/").get_json()["_links"]
    assert links["login"] == {"href": "/v1/auth/login", "type": "POST"}
