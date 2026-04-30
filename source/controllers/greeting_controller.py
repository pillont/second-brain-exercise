import logging
from flask_smorest import Blueprint  # type: ignore[import-untyped]
from dependency_injector.wiring import inject, Provide
from source.container import Container
from source.controllers.entities.greeting_entity import GreetingEntity
from source.controllers.entities.link import Link, Links
from source.controllers.schemas.greeting_schema import GreetingSchema

logger = logging.getLogger(__name__)

greeting_blp = Blueprint("greeting", __name__, url_prefix="")


@greeting_blp.route("/hello", methods=["GET"])
@greeting_blp.response(200, GreetingSchema)
@inject
def get_greeting(
    greeting_service=Provide[Container.greeting_service],
) -> GreetingEntity:
    logger.info("GET /hello endpoint called")
    greeting = greeting_service.get_greeting()
    links = Links(self_link=Link(href="/hello"))
    return GreetingEntity(id=greeting.id, message=greeting.message, links=links)
