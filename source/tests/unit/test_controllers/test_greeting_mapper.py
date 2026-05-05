from source.controllers.v1.entities.greeting_entity import GreetingEntity
from source.controllers.v1.mappers.greeting_mapper import to_greeting_entity
from source.models.greeting import Greeting


def test_to_greeting_entity_maps_fields() -> None:
    greeting = Greeting(id=1, message="Hello from API!")

    result = to_greeting_entity(greeting)

    assert isinstance(result, GreetingEntity)
    assert result.id == 1
    assert result.message == "Hello from API!"


def test_to_greeting_entity_sets_self_link() -> None:
    greeting = Greeting(id=1, message="Hello from API!")

    result = to_greeting_entity(greeting)

    assert result.links["self_link"]["href"] == "/v1/hello"
