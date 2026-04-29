import logging

import pytest
from werkzeug.exceptions import NotFound
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


def test_unexpected_exception_returns_500(app, client):
    @app.route("/boom")
    def boom():
        raise RuntimeError("Unexpected failure")

    response = client.get("/boom")
    assert response.status_code == 500
    assert response.get_json() == {"error": "Internal server error"}


def test_unexpected_exception_is_logged(app, client, caplog):
    @app.route("/boom-log")
    def boom_log():
        raise RuntimeError("logged failure")

    with caplog.at_level(logging.ERROR, logger="source.utils.error_handlers"):
        client.get("/boom-log")

    assert any("logged failure" in record.message for record in caplog.records)


def test_http_exception_is_not_logged_as_error(app, client, caplog):
    @app.route("/not-found")
    def not_found():
        raise NotFound()

    with caplog.at_level(logging.ERROR, logger="source.utils.error_handlers"):
        response = client.get("/not-found")

    assert response.status_code == 404
    assert not any(record.levelno >= logging.ERROR for record in caplog.records)
