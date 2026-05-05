from source.controllers.v1.greeting.greeting_dto import GreetingDTO
from source.controllers.v1.greeting.greeting_mapper import to_greeting_dto
from source.models.greeting import Greeting


def test_to_greeting_dto_maps_fields() -> None:
    greeting = Greeting(id=1, message="Hello from API!")

    result = to_greeting_dto(greeting)

    assert isinstance(result, GreetingDTO)
    assert result.id == 1
    assert result.message == "Hello from API!"


def test_to_greeting_dto_sets_self_link() -> None:
    greeting = Greeting(id=1, message="Hello from API!")

    result = to_greeting_dto(greeting)

    assert result.links["self_link"]["href"] == "/v1/hello"
