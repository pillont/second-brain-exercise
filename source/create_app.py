import logging
from flask import Flask
from flask_smorest import Api  # type: ignore[import-untyped]
from source.config import Config
from source.container import setup_container, Container
from source.controllers.greeting_controller import greeting_blp
from source.controllers.utils.error_handlers import register_error_handlers


class FlaskApp(Flask):
    container: Container


def create_app(config_obj: Config) -> FlaskApp:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    logger = logging.getLogger(__name__)

    app = FlaskApp(__name__)
    app.config.from_object(config_obj)
    logger.info(
        f"Configuration loaded: DEBUG={app.config['DEBUG']},"
        f" TESTING={app.config['TESTING']}"
    )

    logger.info("Initializing dependency injection container...")
    app.container = setup_container()

    logger.info("Registering blueprints...")
    api = Api(app)
    api.register_blueprint(greeting_blp)

    logger.info("Blueprints registered successfully")

    register_error_handlers(app)

    return app
