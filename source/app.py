import logging
from logging import Logger
from source.create_app import create_app
from source.config.app_config import get_app_config
from source.config.flask_config import get_flask_config


def _init_logger() -> Logger:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    return logging.getLogger(__name__)


if __name__ == "__main__":
    logger = _init_logger()
    app_config = get_app_config()
    app = create_app(get_flask_config(app_config), app_config)

    logger.info("Starting Flask server...")
    app.run(host="127.0.0.1", port=5001, debug=True)
