from source.controllers.v1.entities.entry_point_entity import (
    EntryPointEntity, EntryPointLinksEntity)
from source.controllers.v1.entities.link import HttpMethod, LinkEntity


def _build_links() -> EntryPointLinksEntity:
    return EntryPointLinksEntity(
        self_link=LinkEntity(href="/v1/"),
        register=LinkEntity(href="/v1/auth/register", type=HttpMethod.POST),
        login=LinkEntity(href="/v1/auth/login", type=HttpMethod.POST),
    )


def to_entry_point_entity() -> EntryPointEntity:
    return EntryPointEntity(links=_build_links())
