from dataclasses import dataclass
from source.controllers.entities.link import Links


@dataclass
class GreetingEntity:
    id: int
    message: str
    links: Links
