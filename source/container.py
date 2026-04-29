import logging
from dependency_injector import containers, providers
from source.services.greeting_service import GreetingService

logger = logging.getLogger(__name__)


class Container(containers.DeclarativeContainer):
    greeting_service = providers.Singleton(GreetingService)


def setup_container() -> Container:
    logger.info("Setting up dependency injection container...")

    container = Container()
    container.wire(
        modules=[
            "source.controllers.greeting_controller",
        ]
    )

    logger.info("Dependency injection container wired successfully")
    return container
