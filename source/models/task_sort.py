from enum import StrEnum
from typing import Final, Iterable, List

from source.models.task import Task


class SortField(StrEnum):
    ID = "id"
    TITLE = "title"
    DUE_DATE = "due_date"
    STATUS = "status"


class SortDirection(StrEnum):
    ASC = "asc"
    DESC = "desc"


def _sort_by_id(elements: List[Task], reverse: bool) -> List[Task]:
    return sorted(elements, key=lambda t: t.id, reverse=reverse)


def _sort_by_title(elements: List[Task], reverse: bool) -> List[Task]:
    return sorted(elements, key=lambda t: t.title.lower(), reverse=reverse)


def _sort_by_due_date(elements: List[Task], reverse: bool) -> List[Task]:
    return sorted(elements, key=lambda t: t.due_date, reverse=reverse)


def _sort_by_status(elements: List[Task], reverse: bool) -> List[Task]:
    return sorted(elements, key=lambda t: t.status, reverse=reverse)


class TaskSort:
    def __init__(
        self,
        field: SortField = SortField.ID,
        direction: SortDirection = SortDirection.ASC,
    ) -> None:
        self.field: Final = field
        self.direction: Final = direction

    def apply(self, elements: Iterable[Task]) -> List[Task]:
        reverse = self.direction == SortDirection.DESC

        items = list(elements)

        match self.field:
            case SortField.TITLE:
                return _sort_by_title(items, reverse)
            case SortField.DUE_DATE:
                return _sort_by_due_date(items, reverse)
            case SortField.STATUS:
                return _sort_by_status(items, reverse)
            case _:
                return _sort_by_id(items, reverse)
