from typing import TypedDict

from source.controllers.entities.link import LinkEntity, LinksEntity


class EntryPointLinksEntity(LinksEntity):
    register: LinkEntity
    login: LinkEntity


class EntryPointEntity(TypedDict):
    links: EntryPointLinksEntity
