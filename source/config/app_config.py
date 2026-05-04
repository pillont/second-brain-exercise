import os
import logging
from typing import NotRequired, TypedDict


class AppConfig(TypedDict):
    LOG_LEVEL: int
    JWT_SECRET_KEY: str
    DATABASE_URL: NotRequired[str]


JWT_SECRET_KEY: str = os.environ.get(
    "JWT_SECRET_KEY", "dev-jwt-secret-change-in-production"
)


def _get_database_url() -> str:
    return os.environ.get("DATABASE_URL", "sqlite:///tasks.db")


def get_app_config(config_name: str = "development") -> AppConfig:
    match config_name:
        case "development":
            return {
                "LOG_LEVEL": logging.DEBUG,
                "JWT_SECRET_KEY": JWT_SECRET_KEY,
                "DATABASE_URL": _get_database_url(),
            }

        case "testing":
            return {
                "LOG_LEVEL": logging.WARNING,
                "JWT_SECRET_KEY": "test-jwt-secret",
            }

        case "production":
            return {
                "LOG_LEVEL": logging.INFO,
                "JWT_SECRET_KEY": JWT_SECRET_KEY,
                "DATABASE_URL": _get_database_url(),
            }

        case "default":
            return {
                "LOG_LEVEL": logging.INFO,
                "JWT_SECRET_KEY": JWT_SECRET_KEY,
                "DATABASE_URL": _get_database_url(),
            }

        case _:
            raise NotImplementedError()
