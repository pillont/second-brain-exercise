from source.models.greeting import Greeting
from source.controllers.entities.greeting_entity import GreetingEntity
from source.controllers.entities.link import Link, Links


def _build_links() -> Links:
    return Links(self_link=Link(href="/hello"))


def to_greeting_entity(greeting: Greeting) -> GreetingEntity:
    links = _build_links()
    return GreetingEntity(id=greeting.id, message=greeting.message, links=links)
