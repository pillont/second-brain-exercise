import os
import logging

logger = logging.getLogger(__name__)


class Config:
    DEBUG = False
    TESTING = False
    LOG_LEVEL = logging.INFO
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")
    API_TITLE = "My API"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.0.3"
    OPENAPI_URL_PREFIX = "/"
    OPENAPI_SWAGGER_UI_PATH = "/swagger-ui"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"


class DevelopmentConfig(Config):
    DEBUG = True
    LOG_LEVEL = logging.DEBUG


class TestingConfig(Config):
    TESTING = True
    LOG_LEVEL = logging.WARNING


class ProductionConfig(Config):
    DEBUG = False
    LOG_LEVEL = logging.INFO
    SECRET_KEY: str = os.environ.get("SECRET_KEY", "")


config_by_name = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}


def get_config(config_name: str = "development") -> type[Config]:
    return config_by_name.get(config_name, DevelopmentConfig)
