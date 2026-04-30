import os
import logging


class AppConfig:
    LOG_LEVEL: int = logging.INFO
    JWT_SECRET_KEY: str = os.environ.get(
        "JWT_SECRET_KEY", "dev-jwt-secret-change-in-production"
    )


class DevelopmentAppConfig(AppConfig):
    LOG_LEVEL = logging.DEBUG


class TestingAppConfig(AppConfig):
    LOG_LEVEL = logging.WARNING


class ProductionAppConfig(AppConfig):
    pass


_app_configs = {
    "development": DevelopmentAppConfig(),
    "testing": TestingAppConfig(),
    "production": ProductionAppConfig(),
    "default": DevelopmentAppConfig(),
}


def get_app_config(config_name: str = "development") -> AppConfig:
    return _app_configs.get(config_name, DevelopmentAppConfig())
