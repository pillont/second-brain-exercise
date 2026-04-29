import logging
from source.models.greeting import Greeting

logger = logging.getLogger(__name__)


class GreetingService:
    def get_greeting(self) -> Greeting:
        logger.info("GreetingService.get_greeting() called")

        greeting = Greeting(id=1, message="Hello from API!")

        logger.info(f"Returning greeting: id={greeting.id}, message={greeting.message}")
        return greeting
