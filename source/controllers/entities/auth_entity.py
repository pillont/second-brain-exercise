from typing import TypedDict

from source.controllers.entities.link import LinkEntity, LinksEntity


class UserLinksEntity(LinksEntity):
    login: LinkEntity


class AuthDataEntity(TypedDict):
    username: str
    password: str


class UserEntity(TypedDict):
    id: int
    username: str
    links: UserLinksEntity


class TokenLinksEntity(LinksEntity):
    register: LinkEntity
    get_all_tasks: LinkEntity
    create_task: LinkEntity


class TokenEntity(TypedDict):
    token: str
    links: TokenLinksEntity
