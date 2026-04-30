from unittest.mock import MagicMock

import pytest
from source.create_app import create_app
from source.config.config import TestingConfig


@pytest.fixture
def app():
    application = create_app(TestingConfig())
    application.config["TESTING"] = True
    return application


@pytest.fixture
def client(app):
    return app.test_client()


VALID_BODY = {
    "title": "Buy milk",
    "description": "At the store",
    "due_date": "2026-05-01",
}


def test_post_task_returns_201(client) -> None:
    response = client.post("/tasks/", json=VALID_BODY)

    assert response.status_code == 201


def test_post_task_returns_json_with_expected_keys(client) -> None:
    response = client.post("/tasks/", json=VALID_BODY)
    data = response.get_json()

    assert "id" in data
    assert "title" in data
    assert "status" in data
    assert "_links" in data


def test_post_task_status_is_incomplete(client) -> None:
    response = client.post("/tasks/", json=VALID_BODY)
    data = response.get_json()

    assert data["status"] == "Incomplete"


def test_post_task_missing_title_returns_422(client) -> None:
    response = client.post(
        "/tasks/", json={"description": "No title", "due_date": "2026-05-01"}
    )

    assert response.status_code == 422


def test_post_task_service_error_returns_500(app) -> None:
    mock_service = MagicMock()
    mock_service.create_task.side_effect = RuntimeError("Service failure")
    with app.test_client() as client:
        with app.container.create_task_service.override(mock_service):
            response = client.post("/tasks/", json=VALID_BODY)
        assert response.status_code == 500
        data = response.get_json()
        assert "error" in data
