from typing import TypedDict

from source.controllers.v1.utils.link import LinkDTO, LinksListDTO


class EntryPointLinksDTO(LinksListDTO):
    register: LinkDTO
    login: LinkDTO


class EntryPointDTO(TypedDict):
    links: EntryPointLinksDTO
