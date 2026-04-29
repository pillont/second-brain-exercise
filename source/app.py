import logging
from source.create_app import create_app
from source.config import get_config

logger = logging.getLogger(__name__)


if __name__ == "__main__":

    config = get_config()
    app = create_app(config)

    logger.info("Starting Flask server...")
    app.run(host="127.0.0.1", port=5001, debug=True)
