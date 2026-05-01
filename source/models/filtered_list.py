from itertools import islice
from typing import Final, Generic, Iterable, List, Optional, Tuple, TypeVar

T = TypeVar("T")

class FilteredList(Generic[T]):
    def __init__(self, sliced_elements: Iterable[T], has_next: bool) -> None:
        self.elements: Final = sliced_elements
        self.has_next: Final = has_next

def map_to_filtered(
    elements: Iterable[T], page_size: Optional[int]
) -> FilteredList[T]:
    sliced_elements, has_next = _slice_with_has_next(elements, page_size)
    return FilteredList(sliced_elements, has_next)


def _slice_with_has_next(
    elements: Iterable[T], page_size: Optional[int]
) -> Tuple[Iterable[T], bool]:
    if not page_size:
        # CASE : page_size not defined
        return elements, False

    elements_with_next = list(islice(elements, page_size + 1))
    if not _has_next(elements_with_next, page_size):
        # CASE : page_size defined and go to end
        return elements_with_next, False

    # CASE : page_size defined and stop before end
    return islice(elements_with_next, page_size), True


def _has_next(elements_with_next: List[T], page_size: int) -> bool:
    return len(elements_with_next) > page_size


