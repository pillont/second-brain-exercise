from source.models.greeting import Greeting
from source.services.greeting_service import GreetingService


def test_get_greeting_returns_greeting():
    service = GreetingService()
    result = service.get_greeting()
    assert isinstance(result, Greeting)


def test_get_greeting_id():
    service = GreetingService()
    result = service.get_greeting()
    assert result.id == 1


def test_get_greeting_message():
    service = GreetingService()
    result = service.get_greeting()
    assert result.message == "Hello from API!"
