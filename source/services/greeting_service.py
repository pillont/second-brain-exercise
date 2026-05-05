import logging

from source.models.greeting import Greeting

logger = logging.getLogger(__name__)


class GreetingService:
    def get_greeting(self) -> Greeting:
        logger.info("GreetingService.get_greeting() called")

        greeting = Greeting(id=1, message="Hello from API!")

        logger.info(
            "Returning greeting: id=%s, message=%s", greeting.id, greeting.message
        )
        return greeting
