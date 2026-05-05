from source.controllers.v1.root.entry_point_dto import (
    EntryPointDTO,
    EntryPointLinksDTO,
)
from source.controllers.v1.utils.link import HttpMethod, LinkDTO


def _build_links() -> EntryPointLinksDTO:
    return EntryPointLinksDTO(
        self_link=LinkDTO(href="/v1/"),
        register=LinkDTO(href="/v1/auth/register", type=HttpMethod.POST),
        login=LinkDTO(href="/v1/auth/login", type=HttpMethod.POST),
    )


def to_entry_point_dto() -> EntryPointDTO:
    return EntryPointDTO(links=_build_links())
