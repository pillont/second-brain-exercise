from typing import Optional, TypedDict


class ListArgumentEntity(TypedDict):
    cursor: Optional[int]
    page_size: Optional[int]
