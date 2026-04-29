import logging
from flask_smorest import Blueprint  # type: ignore[import-untyped]
from dependency_injector.wiring import inject, Provide
from source.container import Container
from source.models.greeting import Greeting
from source.controllers.schemas.greeting_schema import GreetingSchema

logger = logging.getLogger(__name__)

greeting_blp = Blueprint("greeting", __name__, url_prefix="")


@greeting_blp.route("/hello", methods=["GET"])
@greeting_blp.response(200, GreetingSchema)
@inject
def get_greeting(
    greeting_service=Provide[Container.greeting_service],
) -> Greeting:
    logger.info("GET /hello endpoint called")
    return greeting_service.get_greeting()
