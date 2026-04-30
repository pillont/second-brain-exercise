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


def test_get_tasks_returns_200(client) -> None:
    response = client.get("/tasks/")

    assert response.status_code == 200


def test_get_tasks_returns_empty_list_initially(client) -> None:
    response = client.get("/tasks/")
    data = response.get_json()

    assert isinstance(data, list)
    assert len(data) == 0


def test_get_tasks_returns_list_of_tasks(client) -> None:
    client.post("/tasks/", json=VALID_BODY)
    client.post("/tasks/", json={**VALID_BODY, "title": "Buy eggs"})

    response = client.get("/tasks/")
    data = response.get_json()

    assert isinstance(data, list)
    assert len(data) == 2


def test_get_tasks_each_task_has_expected_keys(client) -> None:
    client.post("/tasks/", json=VALID_BODY)

    response = client.get("/tasks/")
    data = response.get_json()

    assert len(data) == 1
    task = data[0]
    assert "id" in task
    assert "title" in task
    assert "description" in task
    assert "due_date" in task
    assert "status" in task
    assert "_links" in task


def test_get_tasks_each_task_has_self_link(client) -> None:
    client.post("/tasks/", json=VALID_BODY)
    response = client.post("/tasks/", json={**VALID_BODY, "title": "Buy eggs"})
    created_task = response.get_json()
    created_id = created_task["id"]

    response = client.get("/tasks/")
    data = response.get_json()

    task_links = [task["_links"]["self"]["href"] for task in data]
    assert f"/tasks/{created_id}" in task_links


def test_get_tasks_returns_json_content_type(client) -> None:
    response = client.get("/tasks/")

    assert response.content_type == "application/json"


def test_get_tasks_service_error_returns_500(app) -> None:
    mock_service = MagicMock()
    mock_service.get_all_tasks.side_effect = RuntimeError("Service failure")
    with app.test_client() as client:
        with app.container.get_all_tasks_service.override(mock_service):
            response = client.get("/tasks/")
        assert response.status_code == 500
        data = response.get_json()
        assert "error" in data
