import logging

from dependency_injector.wiring import Provide, inject
from flask_smorest import Blueprint

from source.container import Container
from source.controllers.v1.greeting.greeting_entity import GreetingEntity
from source.controllers.v1.greeting.greeting_mapper import to_greeting_entity
from source.controllers.v1.greeting.greeting_schema import GreetingSchema

logger = logging.getLogger(__name__)

v1_greeting_blp = Blueprint("greeting", __name__, url_prefix="")


@v1_greeting_blp.route("/v1/hello", methods=["GET"])
@v1_greeting_blp.doc(summary="Greeting", description="Returns a greeting message.")
@v1_greeting_blp.response(200, GreetingSchema)
@inject
def get_greeting(
    greeting_service=Provide[Container.greeting_service],
) -> GreetingEntity:
    return to_greeting_entity(greeting_service.get_greeting())
