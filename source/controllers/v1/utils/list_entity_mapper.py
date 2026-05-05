from typing import TypeVar

from source.controllers.v1.utils.list_entity import ListEntity
from source.models.filtered_list import FilteredList

T = TypeVar("T")


def map_to_list_entity(filtered_list: FilteredList[T]) -> ListEntity[T]:
    return ListEntity[T](
        elements=filtered_list.elements,
        has_next=filtered_list.has_next,
        next_cursor=filtered_list.next_cursor,
    )
