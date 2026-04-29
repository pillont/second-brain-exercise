import logging
from flask import Flask, Response, jsonify, make_response
from werkzeug.exceptions import HTTPException

logger = logging.getLogger(__name__)


def register_error_handlers(app: Flask) -> None:
    @app.errorhandler(Exception)
    def handle_unexpected_error(
        e: Exception,
    ) -> tuple[Response, int] | Response:
        if isinstance(e, HTTPException):
            return make_response(e.get_response(), e.code or 500)
        logger.error("Unexpected error: %s", str(e), exc_info=True)
        return jsonify({"error": "Internal server error"}), 500
