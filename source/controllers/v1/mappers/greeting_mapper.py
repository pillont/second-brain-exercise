from source.models.greeting import Greeting
from source.controllers.v1.entities.greeting_entity import GreetingEntity
from source.controllers.v1.entities.link import LinkEntity, LinksEntity


def _build_links() -> LinksEntity:
    return LinksEntity(self_link=LinkEntity(href="/v1/hello"))


def to_greeting_entity(greeting: Greeting) -> GreetingEntity:
    links = _build_links()
    return GreetingEntity(id=greeting.id, message=greeting.message, links=links)
