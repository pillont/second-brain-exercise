from typing import TypedDict

from source.controllers.v1.utils.link import LinkDTO, LinksListDTO


class UserLinksDTO(LinksListDTO):
    login: LinkDTO


class AuthDataDTO(TypedDict):
    username: str
    password: str


class UserDTO(TypedDict):
    id: int
    username: str
    links: UserLinksDTO


class TokenLinksDTO(LinksListDTO):
    register: LinkDTO
    get_all_tasks: LinkDTO
    create_task: LinkDTO


class TokenDTO(TypedDict):
    token: str
    links: TokenLinksDTO
