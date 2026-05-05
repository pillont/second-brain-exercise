from dataclasses import dataclass, field
from typing import Generic, Iterable, Optional, TypeVar

T = TypeVar("T")


@dataclass
class ListEntity(Generic[T]):
    elements: Iterable[T]
    has_next: bool
    next_cursor: Optional[str] = field(default=None)
