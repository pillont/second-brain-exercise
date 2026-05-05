from enum import StrEnum
from typing import NotRequired, TypedDict


class HttpMethod(StrEnum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"


class LinkDTO(TypedDict):
    href: str
    type: NotRequired[HttpMethod]


class LinksListDTO(TypedDict):
    self_link: LinkDTO
