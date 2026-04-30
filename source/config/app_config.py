import os
import logging
from typing import TypedDict


class AppConfig(TypedDict):
    LOG_LEVEL: int
    JWT_SECRET_KEY: str


JWT_SECRET_KEY: str = os.environ.get(
    "JWT_SECRET_KEY", "dev-jwt-secret-change-in-production"
)


def get_app_config(config_name: str = "development") -> AppConfig:
    match config_name:
        case "development":
            return {"LOG_LEVEL": logging.DEBUG, "JWT_SECRET_KEY": JWT_SECRET_KEY}

        case "testing":
            return {
                "LOG_LEVEL": logging.WARNING,
                "JWT_SECRET_KEY": "test-jwt-secret",
            }

        case "production":
            return {"LOG_LEVEL": logging.INFO, "JWT_SECRET_KEY": JWT_SECRET_KEY}

        case "default":
            return {"LOG_LEVEL": logging.INFO, "JWT_SECRET_KEY": JWT_SECRET_KEY}

        case _:
            raise NotImplementedError()
