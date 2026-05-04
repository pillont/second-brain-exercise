import importlib
import logging
import pkgutil
from typing import Iterator

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_smorest import Api, Blueprint

import source.controllers.v1
from source.config.app_config import AppConfig
from source.config.flask_config import FlaskConfig
from source.container import setup_container, Container
from source.controllers.utils.error_handlers import register_error_handlers
from source.controllers.utils.request_logger import register_request_logger

logger = logging.getLogger(__name__)


class FlaskApp(Flask):
    container: Container


jwt = JWTManager()


def _init_app(flask_config: FlaskConfig, app_config: AppConfig) -> FlaskApp:
    app = FlaskApp(__name__)
    app.config.from_object(flask_config)

    app.container = setup_container(app_config)

    jwt.init_app(app)

    return app


def _register_module_blueprints(api: Api, module: object) -> None:
    for attr_name in dir(module):
        attr = getattr(module, attr_name)
        if isinstance(attr, Blueprint):
            api.register_blueprint(attr)


def _iter_controller_modules() -> Iterator[pkgutil.ModuleInfo]:
    controllers = pkgutil.walk_packages(
        path=source.controllers.__path__,
        prefix="source.controllers.",
    )
    return controllers



def _register_blueprints(app: FlaskApp) -> None:
    api = Api(app)
    for info in _iter_controller_modules():
        module = importlib.import_module(info.name)
        _register_module_blueprints(api, module)


def _register_utils(app: FlaskApp) -> None:
    register_error_handlers(app)
    register_request_logger(app)


def create_app(flask_config: FlaskConfig, app_config: AppConfig) -> FlaskApp:

    app = _init_app(flask_config, app_config)
    logger.info(
        "Configuration loaded: DEBUG=%s, TESTING=%s",
        app.config["DEBUG"],
        app.config["TESTING"],
    )

    logger.info("Registering blueprints...")
    _register_blueprints(app)
    logger.info("Blueprints registered successfully")

    _register_utils(app)

    return app
