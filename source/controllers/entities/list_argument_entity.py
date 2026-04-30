from typing import Optional, TypedDict


class ListArgumentEntity(TypedDict):
    page_size: Optional[int]
    cursor: Optional[int]
