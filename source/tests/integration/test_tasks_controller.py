from unittest.mock import MagicMock

import pytest
from source.config.flask_config import TestingFlaskConfig
from source.config.app_config import get_app_config
from source.create_app import create_app


@pytest.fixture
def app():
    application = create_app(TestingFlaskConfig(), get_app_config("testing"))
    application.config["TESTING"] = True
    return application


USER_CREDENTIALS = {"username": "taskuser", "password": "taskpass"}


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


@pytest.fixture
def unauthenticated_client(app):
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


def test_post_task_service_error_returns_500(app, token) -> None:
    mock_service = MagicMock()
    mock_service.create_task.side_effect = RuntimeError("Service failure")
    with app.test_client() as client:
        client.environ_base["HTTP_AUTHORIZATION"] = f"Bearer {token}"
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
    data = response.get_json()["elements"]

    assert isinstance(data, list)
    assert len(data) == 0


def test_get_tasks_returns_list_of_tasks(client) -> None:
    client.post("/tasks/", json=VALID_BODY)
    client.post("/tasks/", json={**VALID_BODY, "title": "Buy eggs"})

    response = client.get("/tasks/")
    data = response.get_json()["elements"]

    assert isinstance(data, list)
    assert len(data) == 2


def test_get_tasks_each_task_has_expected_keys(client) -> None:
    client.post("/tasks/", json=VALID_BODY)

    response = client.get("/tasks/")
    data = response.get_json()["elements"]

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
    data = response.get_json()["elements"]

    task_links = [task["_links"]["self"]["href"] for task in data]
    assert f"/tasks/{created_id}" in task_links


def test_get_tasks_each_task_has_tasks_link(client) -> None:
    client.post("/tasks/", json=VALID_BODY)

    response = client.get("/tasks/")
    data = response.get_json()["elements"]

    assert data[0]["_links"]["tasks"]["href"] == "/tasks/"


def test_post_task_response_has_tasks_link(client) -> None:
    response = client.post("/tasks/", json=VALID_BODY)
    data = response.get_json()

    assert data["_links"]["tasks"]["href"] == "/tasks/"


def test_get_tasks_returns_json_content_type(client) -> None:
    response = client.get("/tasks/")

    assert response.content_type == "application/json"


def test_get_tasks_service_error_returns_500(app, token) -> None:
    mock_service = MagicMock()
    mock_service.get_all_tasks.side_effect = RuntimeError("Service failure")
    with app.test_client() as client:
        client.environ_base["HTTP_AUTHORIZATION"] = f"Bearer {token}"
        with app.container.get_all_tasks_service.override(mock_service):
            response = client.get("/tasks/")
        assert response.status_code == 500
        data = response.get_json()
        assert "error" in data


def test_get_task_returns_200(client) -> None:
    created = client.post("/tasks/", json=VALID_BODY).get_json()

    response = client.get(f"/tasks/{created['id']}")

    assert response.status_code == 200


def test_get_task_returns_expected_keys(client) -> None:
    created = client.post("/tasks/", json=VALID_BODY).get_json()

    response = client.get(f"/tasks/{created['id']}")
    data = response.get_json()

    assert "id" in data
    assert "title" in data
    assert "description" in data
    assert "due_date" in data
    assert "status" in data
    assert "_links" in data


def test_get_task_returns_correct_task(client) -> None:
    created = client.post("/tasks/", json=VALID_BODY).get_json()

    response = client.get(f"/tasks/{created['id']}")
    data = response.get_json()

    assert data["id"] == created["id"]
    assert data["title"] == VALID_BODY["title"]


def test_get_task_returns_self_link(client) -> None:
    created = client.post("/tasks/", json=VALID_BODY).get_json()

    response = client.get(f"/tasks/{created['id']}")
    data = response.get_json()

    assert data["_links"]["self"]["href"] == f"/tasks/{created['id']}"


def test_get_task_returns_tasks_link(client) -> None:
    created = client.post("/tasks/", json=VALID_BODY).get_json()

    response = client.get(f"/tasks/{created['id']}")
    data = response.get_json()

    assert data["_links"]["tasks"]["href"] == "/tasks/"


def test_get_task_returns_404_when_not_found(client) -> None:
    response = client.get("/tasks/999")

    assert response.status_code == 404


def test_get_task_service_error_returns_500(app, token) -> None:
    mock_service = MagicMock()
    mock_service.get_task.side_effect = RuntimeError("Service failure")
    with app.test_client() as client:
        client.environ_base["HTTP_AUTHORIZATION"] = f"Bearer {token}"
        with app.container.get_task_service.override(mock_service):
            response = client.get("/tasks/1")
        assert response.status_code == 500
        data = response.get_json()
        assert "error" in data


def test_post_task_response_has_update_link(client) -> None:
    response = client.post("/tasks/", json=VALID_BODY)
    data = response.get_json()

    assert "_links" in data
    assert "update" in data["_links"]
    assert "href" in data["_links"]["update"]


def test_get_task_returns_update_link(client) -> None:
    created = client.post("/tasks/", json=VALID_BODY).get_json()

    response = client.get(f"/tasks/{created['id']}")
    data = response.get_json()

    assert data["_links"]["update"]["href"] == f"/tasks/{created['id']}"
    assert data["_links"]["update"]["type"] == "PUT"


def test_get_tasks_each_task_has_update_link(client) -> None:
    client.post("/tasks/", json=VALID_BODY)

    response = client.get("/tasks/")
    data = response.get_json()["elements"]

    assert "update" in data[0]["_links"]


VALID_UPDATE_BODY = {
    "title": "Buy eggs",
    "description": "At the market",
    "due_date": "2026-06-01",
    "status": "Complete",
}


def test_put_task_returns_204(client) -> None:
    created = client.post("/tasks/", json=VALID_BODY).get_json()

    response = client.put(f"/tasks/{created['id']}", json=VALID_UPDATE_BODY)

    assert response.status_code == 204


def test_put_task_updates_title(client) -> None:
    created = client.post("/tasks/", json=VALID_BODY).get_json()

    client.put(f"/tasks/{created['id']}", json=VALID_UPDATE_BODY)
    data = client.get(f"/tasks/{created['id']}").get_json()

    assert data["title"] == "Buy eggs"


def test_put_task_updates_description(client) -> None:
    created = client.post("/tasks/", json=VALID_BODY).get_json()

    client.put(f"/tasks/{created['id']}", json=VALID_UPDATE_BODY)
    data = client.get(f"/tasks/{created['id']}").get_json()

    assert data["description"] == "At the market"


def test_put_task_updates_due_date(client) -> None:
    created = client.post("/tasks/", json=VALID_BODY).get_json()

    client.put(f"/tasks/{created['id']}", json=VALID_UPDATE_BODY)
    data = client.get(f"/tasks/{created['id']}").get_json()

    assert data["due_date"] == "2026-06-01"


def test_put_task_updates_status_to_complete(client) -> None:
    created = client.post("/tasks/", json=VALID_BODY).get_json()

    client.put(f"/tasks/{created['id']}", json=VALID_UPDATE_BODY)
    data = client.get(f"/tasks/{created['id']}").get_json()

    assert data["status"] == "Complete"


def test_put_task_returns_404_when_not_found(client) -> None:
    response = client.put("/tasks/999", json=VALID_UPDATE_BODY)

    assert response.status_code == 404


def test_put_task_missing_status_returns_422(client) -> None:
    created = client.post("/tasks/", json=VALID_BODY).get_json()
    body = {k: v for k, v in VALID_UPDATE_BODY.items() if k != "status"}

    response = client.put(f"/tasks/{created['id']}", json=body)

    assert response.status_code == 422


def test_put_task_missing_title_returns_422(client) -> None:
    created = client.post("/tasks/", json=VALID_BODY).get_json()
    body = {k: v for k, v in VALID_UPDATE_BODY.items() if k != "title"}

    response = client.put(f"/tasks/{created['id']}", json=body)

    assert response.status_code == 422


def test_put_task_service_error_returns_500(app, token) -> None:
    mock_service = MagicMock()
    mock_service.update_task.side_effect = RuntimeError("Service failure")
    with app.test_client() as client:
        client.environ_base["HTTP_AUTHORIZATION"] = f"Bearer {token}"
        created = client.post("/tasks/", json=VALID_BODY).get_json()
        with app.container.update_task_service.override(mock_service):
            response = client.put(f"/tasks/{created['id']}", json=VALID_UPDATE_BODY)
        assert response.status_code == 500
        data = response.get_json()
        assert "error" in data


def test_delete_task_returns_204(client) -> None:
    created = client.post("/tasks/", json=VALID_BODY).get_json()

    response = client.delete(f"/tasks/{created['id']}")

    assert response.status_code == 204


def test_delete_task_removes_task_from_list(client) -> None:
    created = client.post("/tasks/", json=VALID_BODY).get_json()

    client.delete(f"/tasks/{created['id']}")
    data = client.get("/tasks/").get_json()["elements"]

    assert len(data) == 0


def test_delete_task_makes_task_not_found(client) -> None:
    created = client.post("/tasks/", json=VALID_BODY).get_json()

    client.delete(f"/tasks/{created['id']}")
    response = client.get(f"/tasks/{created['id']}")

    assert response.status_code == 404


def test_delete_task_returns_404_when_not_found(client) -> None:
    response = client.delete("/tasks/999")

    assert response.status_code == 404


def test_delete_task_service_error_returns_500(app, token) -> None:
    mock_service = MagicMock()
    mock_service.delete_task.side_effect = RuntimeError("Service failure")
    with app.test_client() as client:
        client.environ_base["HTTP_AUTHORIZATION"] = f"Bearer {token}"
        created = client.post("/tasks/", json=VALID_BODY).get_json()
        with app.container.delete_task_service.override(mock_service):
            response = client.delete(f"/tasks/{created['id']}")
        assert response.status_code == 500
        data = response.get_json()
        assert "error" in data


def test_post_task_response_has_delete_link(client) -> None:
    response = client.post("/tasks/", json=VALID_BODY)
    data = response.get_json()

    assert "delete" in data["_links"]
    assert "href" in data["_links"]["delete"]


def test_get_task_returns_delete_link(client) -> None:
    created = client.post("/tasks/", json=VALID_BODY).get_json()

    response = client.get(f"/tasks/{created['id']}")
    data = response.get_json()

    assert data["_links"]["delete"]["href"] == f"/tasks/{created['id']}"
    assert data["_links"]["delete"]["type"] == "DELETE"


def test_get_tasks_each_task_has_delete_link(client) -> None:
    client.post("/tasks/", json=VALID_BODY)

    response = client.get("/tasks/")
    data = response.get_json()["elements"]

    assert "delete" in data[0]["_links"]


def test_get_tasks_filter_by_status_complete(client) -> None:
    client.post("/tasks/", json=VALID_BODY)
    created = client.post("/tasks/", json={**VALID_BODY, "title": "Buy eggs"}).get_json()
    client.put(f"/tasks/{created['id']}", json=VALID_UPDATE_BODY)

    response = client.get("/tasks/?status=Complete")
    data = response.get_json()["elements"]

    assert len(data) == 1
    assert data[0]["status"] == "Complete"


def test_get_tasks_filter_by_status_incomplete(client) -> None:
    client.post("/tasks/", json=VALID_BODY)
    created = client.post("/tasks/", json={**VALID_BODY, "title": "Buy eggs"}).get_json()
    client.put(f"/tasks/{created['id']}", json=VALID_UPDATE_BODY)

    response = client.get("/tasks/?status=Incomplete")
    data = response.get_json()["elements"]

    assert len(data) == 1
    assert data[0]["status"] == "Incomplete"


def test_get_tasks_filter_by_due_date_from(client) -> None:
    client.post("/tasks/", json={**VALID_BODY, "due_date": "2026-01-01"})
    client.post("/tasks/", json={**VALID_BODY, "due_date": "2026-12-31"})

    response = client.get("/tasks/?due_date_from=2026-06-01")
    data = response.get_json()["elements"]

    assert len(data) == 1
    assert data[0]["due_date"] == "2026-12-31"


def test_get_tasks_filter_by_due_date_to(client) -> None:
    client.post("/tasks/", json={**VALID_BODY, "due_date": "2026-01-01"})
    client.post("/tasks/", json={**VALID_BODY, "due_date": "2026-12-31"})

    response = client.get("/tasks/?due_date_to=2026-06-01")
    data = response.get_json()["elements"]

    assert len(data) == 1
    assert data[0]["due_date"] == "2026-01-01"


def test_get_tasks_filter_by_due_date_range(client) -> None:
    client.post("/tasks/", json={**VALID_BODY, "due_date": "2026-01-01"})
    client.post("/tasks/", json={**VALID_BODY, "due_date": "2026-06-15"})
    client.post("/tasks/", json={**VALID_BODY, "due_date": "2026-12-31"})

    response = client.get("/tasks/?due_date_from=2026-03-01&due_date_to=2026-09-01")
    data = response.get_json()["elements"]

    assert len(data) == 1
    assert data[0]["due_date"] == "2026-06-15"


def test_get_tasks_filter_by_title(client) -> None:
    client.post("/tasks/", json={**VALID_BODY, "title": "Buy milk"})
    client.post("/tasks/", json={**VALID_BODY, "title": "Walk the dog"})

    response = client.get("/tasks/?title=buy")
    data = response.get_json()["elements"]

    assert len(data) == 1
    assert data[0]["title"] == "Buy milk"


def test_get_tasks_filter_by_title_case_insensitive(client) -> None:
    client.post("/tasks/", json={**VALID_BODY, "title": "Buy Milk"})
    client.post("/tasks/", json={**VALID_BODY, "title": "Walk the dog"})

    response = client.get("/tasks/?title=BUY")
    data = response.get_json()["elements"]

    assert len(data) == 1


def test_get_tasks_filter_by_description(client) -> None:
    client.post("/tasks/", json={**VALID_BODY, "description": "At the store"})
    client.post("/tasks/", json={**VALID_BODY, "description": "In the park"})

    response = client.get("/tasks/?description=store")
    data = response.get_json()["elements"]

    assert len(data) == 1
    assert data[0]["description"] == "At the store"


def test_get_tasks_filter_by_description_case_insensitive(client) -> None:
    client.post("/tasks/", json={**VALID_BODY, "description": "At the Store"})
    client.post("/tasks/", json={**VALID_BODY, "description": "In the park"})

    response = client.get("/tasks/?description=STORE")
    data = response.get_json()["elements"]

    assert len(data) == 1


def test_get_tasks_filter_combined_status_and_title(client) -> None:
    client.post("/tasks/", json={**VALID_BODY, "title": "Buy milk"})
    created = client.post("/tasks/", json={**VALID_BODY, "title": "Buy eggs"}).get_json()
    client.put(f"/tasks/{created['id']}", json=VALID_UPDATE_BODY)

    response = client.get("/tasks/?status=Incomplete&title=buy")
    data = response.get_json()["elements"]

    assert len(data) == 1
    assert data[0]["title"] == "Buy milk"


def test_get_tasks_filter_with_pagination(client) -> None:
    client.post("/tasks/", json={**VALID_BODY, "title": "Task 1"})
    client.post("/tasks/", json={**VALID_BODY, "title": "Task 2"})
    created = client.post("/tasks/", json={**VALID_BODY, "title": "Task 3"}).get_json()
    client.put(f"/tasks/{created['id']}", json=VALID_UPDATE_BODY)

    response = client.get("/tasks/?status=Incomplete&page_size=1")
    data = response.get_json()

    assert len(data["elements"]) == 1
    assert data["has_next"] is True


def test_get_tasks_filter_returns_empty_list_when_no_match(client) -> None:
    client.post("/tasks/", json=VALID_BODY)

    response = client.get("/tasks/?status=Complete")
    data = response.get_json()

    assert data["elements"] == []
    assert data["has_next"] is False


def test_get_tasks_filter_returns_multiple_matching_elements(client) -> None:
    client.post("/tasks/", json={**VALID_BODY, "title": "Task 1"})
    client.post("/tasks/", json={**VALID_BODY, "title": "Task 2"})
    created = client.post("/tasks/", json={**VALID_BODY, "title": "Task 3"}).get_json()
    client.put(f"/tasks/{created['id']}", json=VALID_UPDATE_BODY)

    response = client.get("/tasks/?status=Incomplete")
    data = response.get_json()

    assert len(data["elements"]) == 2
    assert data["has_next"] is False


def test_get_tasks_filter_invalid_status_returns_422(client) -> None:
    response = client.get("/tasks/?status=Invalid")

    assert response.status_code == 422


def test_post_task_without_auth_returns_401(unauthenticated_client) -> None:
    response = unauthenticated_client.post("/tasks/", json=VALID_BODY)

    assert response.status_code == 401


def test_get_tasks_without_auth_returns_401(unauthenticated_client) -> None:
    response = unauthenticated_client.get("/tasks/")

    assert response.status_code == 401


def test_get_task_without_auth_returns_401(unauthenticated_client) -> None:
    response = unauthenticated_client.get("/tasks/1")

    assert response.status_code == 401


def test_put_task_without_auth_returns_401(unauthenticated_client) -> None:
    response = unauthenticated_client.put("/tasks/1", json=VALID_UPDATE_BODY)

    assert response.status_code == 401


def test_delete_task_without_auth_returns_401(unauthenticated_client) -> None:
    response = unauthenticated_client.delete("/tasks/1")

    assert response.status_code == 401
