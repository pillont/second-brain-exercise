from typing import Optional, TypedDict


class ListArgumentDTO(TypedDict):
    cursor: Optional[str]
    page_size: Optional[int]
