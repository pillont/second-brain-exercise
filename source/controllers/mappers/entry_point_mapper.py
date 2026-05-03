from source.controllers.entities.entry_point_entity import (
    EntryPointEntity,
    EntryPointLinksEntity,
)
from source.controllers.entities.link import HttpMethod, LinkEntity


def _build_links() -> EntryPointLinksEntity:
    return EntryPointLinksEntity(
        self_link=LinkEntity(href="/"),
        register=LinkEntity(href="/auth/register", type=HttpMethod.POST),
        login=LinkEntity(href="/auth/login", type=HttpMethod.POST),
    )


def to_entry_point_entity() -> EntryPointEntity:
    return EntryPointEntity(links=_build_links())
