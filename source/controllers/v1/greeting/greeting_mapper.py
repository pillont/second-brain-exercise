from source.controllers.v1.greeting.greeting_dto import GreetingDTO
from source.controllers.v1.utils.link import LinkDTO, LinksListDTO
from source.models.greeting import Greeting


def _build_links() -> LinksListDTO:
    return LinksListDTO(self_link=LinkDTO(href="/v1/hello"))


def to_greeting_dto(greeting: Greeting) -> GreetingDTO:
    links = _build_links()
    return GreetingDTO(id=greeting.id, message=greeting.message, links=links)
