from dataclasses import dataclass
from enum import StrEnum
from typing import NotRequired, TypedDict


class HttpMethod(StrEnum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"

class LinkEntity(TypedDict):
    href: str
    type: NotRequired[HttpMethod]


class LinksEntity(TypedDict):
    self_link: LinkEntity
