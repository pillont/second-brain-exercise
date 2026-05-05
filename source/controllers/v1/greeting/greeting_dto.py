from dataclasses import dataclass

from source.controllers.v1.utils.link import LinksListDTO


@dataclass
class GreetingDTO:
    id: int
    message: str
    links: LinksListDTO
