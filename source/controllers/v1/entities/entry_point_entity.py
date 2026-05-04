from typing import TypedDict

from source.controllers.v1.entities.link import LinkEntity, LinksEntity


class EntryPointLinksEntity(LinksEntity):
    register: LinkEntity
    login: LinkEntity


class EntryPointEntity(TypedDict):
    links: EntryPointLinksEntity
