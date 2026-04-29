import os
import logging


class Config:
    DEBUG = False
    TESTING = False
    LOG_LEVEL = logging.INFO
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")


class DevelopmentConfig(Config):
    DEBUG = True
    LOG_LEVEL = logging.DEBUG


class TestingConfig(Config):
    TESTING = True
    LOG_LEVEL = logging.WARNING


class ProductionConfig(Config):
    DEBUG = False
    LOG_LEVEL = logging.INFO
    SECRET_KEY = os.environ.get("SECRET_KEY")


config_by_name = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}


def get_config(config_name: str) -> Config:
    if config_name is None:
        config_name = os.environ.get("FLASK_ENV", "development")

    return config_by_name.get(config_name, DevelopmentConfig)
