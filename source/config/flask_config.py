from datetime import timedelta
import os

from source.config.app_config import AppConfig


class FlaskConfig:
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")
    API_TITLE = "My API"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.0.3"
    OPENAPI_URL_PREFIX = "/"
    OPENAPI_SWAGGER_UI_PATH = "/swagger-ui"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    API_SPEC_OPTIONS = {
        "components": {
            "securitySchemes": {
                "BearerAuth": {
                    "type": "http",
                    "scheme": "bearer",
                    "bearerFormat": "JWT",
                }
            }
        },
        "security": [{"BearerAuth": []}],
    }

    JWT_ACCESS_TOKEN_EXPIRES: timedelta
    JWT_SECRET_KEY: str

class DevelopmentFlaskConfig(FlaskConfig):
    DEBUG = True


class TestingFlaskConfig(FlaskConfig):
    TESTING = True


class ProductionFlaskConfig(FlaskConfig):
    SECRET_KEY: str = os.environ.get("SECRET_KEY", "")


_flask_configs = {
    "development": DevelopmentFlaskConfig(),
    "testing": TestingFlaskConfig(),
    "production": ProductionFlaskConfig(),
    "default": DevelopmentFlaskConfig(),
}


def get_flask_config(app_config: AppConfig, config_name: str = "development") -> FlaskConfig:
    config = _flask_configs.get(config_name, DevelopmentFlaskConfig())

    apply_jwt_config(config, app_config)

    return config

def apply_jwt_config(config:FlaskConfig, app_config:AppConfig )-> None:
    config.JWT_SECRET_KEY = app_config["JWT_SECRET_KEY"]
    config.JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)