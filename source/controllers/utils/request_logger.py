import logging
from flask import Flask, request

logger = logging.getLogger(__name__)


def register_request_logger(app: Flask) -> None:
    @app.before_request
    def log_request() -> None:
        logger.info("%s %s", request.method, request.path)
