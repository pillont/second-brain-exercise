import logging

import pytest
from flask import Flask, Response

from source.config.app_config import get_app_config
from source.config.flask_config import TestingFlaskConfig
from source.controllers.utils.request_logger import register_request_logger
from source.create_app import create_app


@pytest.fixture
def app():
    application = create_app(TestingFlaskConfig(), get_app_config("testing"))
    application.config["TESTING"] = True
    return application


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def slow_app():
    application = Flask(__name__)
    application.config["TESTING"] = True
    register_request_logger(application, slow_threshold_ms=0)

    @application.route("/ping")
    def ping() -> Response:
        return Response("ok", status=200)

    return application


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
            "/v1/tasks/",
            json={"title": "t", "description": "d", "due_date": "2026-05-01"},
        )

    assert any(
        "POST" in record.message and "/v1/tasks/" in record.message
        for record in caplog.records
    )


def test_request_id_is_logged(client, caplog):
    with caplog.at_level(
        logging.INFO, logger="source.controllers.utils.request_logger"
    ):
        client.get("/v1/hello")

    assert any("request_id=" in record.message for record in caplog.records)


def test_response_timing_is_logged(client, caplog):
    with caplog.at_level(
        logging.INFO, logger="source.controllers.utils.request_logger"
    ):
        client.get("/v1/hello")

    assert any(
        "→" in record.message and "ms" in record.message for record in caplog.records
    )


def test_request_id_header_in_response(client):
    response = client.get("/v1/hello")
    assert "X-Request-ID" in response.headers
    assert len(response.headers["X-Request-ID"]) > 0


def test_slow_request_logs_warning(slow_app, caplog):
    with slow_app.test_client() as client:
        with caplog.at_level(
            logging.WARNING, logger="source.controllers.utils.request_logger"
        ):
            client.get("/ping")

    assert any(
        record.levelno == logging.WARNING and "→" in record.message
        for record in caplog.records
    )
