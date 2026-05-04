import logging
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


def test_request_is_logged(client, caplog):
    with caplog.at_level(
        logging.INFO, logger="source.controllers.utils.request_logger"
    ):
        client.get("/v1/hello")

    assert any(
        "GET" in record.message and "/v1/hello" in record.message
        for record in caplog.records
    )


def test_post_request_is_logged(client, caplog):
    with caplog.at_level(
        logging.INFO, logger="source.controllers.utils.request_logger"
    ):
        client.post(
            "/v1/tasks/", json={"title": "t", "description": "d", "due_date": "2026-05-01"}
        )

    assert any(
        "POST" in record.message and "/v1/tasks/" in record.message
        for record in caplog.records
    )
