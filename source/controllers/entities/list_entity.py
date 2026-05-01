from dataclasses import dataclass
from typing import Generic, Iterable, TypeVar

T = TypeVar("T")


@dataclass
class ListEntity(Generic[T]):
    elements: Iterable[T]
    has_next: bool
