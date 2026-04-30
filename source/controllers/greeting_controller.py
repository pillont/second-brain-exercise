import logging
from flask_smorest import Blueprint
from dependency_injector.wiring import inject, Provide
from source.container import Container
from source.controllers.entities.greeting_entity import GreetingEntity
from source.controllers.mappers.greeting_mapper import to_greeting_entity
from source.controllers.schemas.greeting_schema import GreetingSchema

logger = logging.getLogger(__name__)

greeting_blp = Blueprint("greeting", __name__, url_prefix="")


@greeting_blp.route("/hello", methods=["GET"])
@greeting_blp.response(200, GreetingSchema)
@inject
def get_greeting(
    greeting_service=Provide[Container.greeting_service],
) -> GreetingEntity:
    return to_greeting_entity(greeting_service.get_greeting())
