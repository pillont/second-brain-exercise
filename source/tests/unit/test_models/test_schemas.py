import pytest
from source.models.greeting import Greeting
from source.controllers.schemas.greeting_schema import GreetingSchema


@pytest.fixture
def schema() -> GreetingSchema:
    return GreetingSchema()


def test_greeting_schema_dump(schema: GreetingSchema) -> None:
    greeting = Greeting(id=42, message="Hi there")
    result = schema.dump(greeting)
    assert result == {"id": 42, "message": "Hi there"}


def test_greeting_schema_keys(schema: GreetingSchema) -> None:
    greeting = Greeting(id=1, message="test")
    result = schema.dump(greeting)
    assert "id" in result
    assert "message" in result
    assert len(result) == 2


def test_greeting_schema_types(schema: GreetingSchema) -> None:
    greeting = Greeting(id=1, message="Hello")
    result = schema.dump(greeting)
    assert isinstance(result["id"], int)
    assert isinstance(result["message"], str)
