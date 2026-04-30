import logging
from logging import Logger
from source.create_app import create_app
from source.config.config import get_config


def _init_logger() -> Logger:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    return logging.getLogger(__name__)


if __name__ == "__main__":
    logger = _init_logger()
    config = get_config()
    app = create_app(config)

    logger.info("Starting Flask server...")
    app.run(host="127.0.0.1", port=5001, debug=True)
