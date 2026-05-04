from typing import Optional, TypedDict


class ListArgumentEntity(TypedDict):
    cursor: Optional[str]
    page_size: Optional[int]
