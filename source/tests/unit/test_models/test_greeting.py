from source.models.greeting import Greeting


def test_greeting_creation():
    greeting = Greeting(id=1, message="Hello")
    assert greeting.id == 1
    assert greeting.message == "Hello"
