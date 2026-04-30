from dataclasses import dataclass
from source.controllers.entities.link import LinksEntity


@dataclass
class GreetingEntity:
    id: int
    message: str
    links: LinksEntity
