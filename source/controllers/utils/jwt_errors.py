import logging

from flask import Flask, request

from source.create_app import jwt

logger = logging.getLogger(__name__)


def register_error_handlers(app: Flask) -> None:
    @jwt.expired_token_loader
    def expired_callback(jwt_header: dict, jwt_payload: dict) -> tuple:
        logger.warning("Expired JWT token: %s %s", request.method, request.path)
        return {"msg": "Token expiré"}, 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error: str) -> tuple:
        logger.warning(
            "Invalid JWT token: %s %s — %s", request.method, request.path, error
        )
        return {"msg": "Token invalide"}, 422
