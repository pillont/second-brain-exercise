import logging
from flask import Flask
from source.create_app import jwt

logger = logging.getLogger(__name__)


def register_error_handlers(app: Flask) -> None:
    @jwt.expired_token_loader
    def expired_callback(jwt_header, jwt_payload):
        return {"msg": "Token expiré"}, 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return {"msg": "Token invalide"}, 422
