from datetime import date
from typing import Final, Iterable, Optional

from source.models.task import Task, TaskStatus


def _filter_by_status(
    elements: Iterable[Task], status: TaskStatus
) -> Iterable[Task]:
    return (t for t in elements if t.status == status)


def _filter_by_due_date_from(
    elements: Iterable[Task], due_date_from: date
) -> Iterable[Task]:
    return (t for t in elements if t.due_date >= due_date_from)


def _filter_by_due_date_to(
    elements: Iterable[Task], due_date_to: date
) -> Iterable[Task]:
    return (t for t in elements if t.due_date <= due_date_to)


def _filter_by_title(elements: Iterable[Task], title: str) -> Iterable[Task]:
    return (t for t in elements if title.lower() in t.title.lower())


def _filter_by_description(
    elements: Iterable[Task], description: str
) -> Iterable[Task]:
    return (t for t in elements if description.lower() in t.description.lower())


class TaskFilters:
    def __init__(
        self,
        status: Optional[TaskStatus] = None,
        due_date_from: Optional[date] = None,
        due_date_to: Optional[date] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
    ) -> None:
        self.status: Final = status
        self.due_date_from: Final = due_date_from
        self.due_date_to: Final = due_date_to
        self.title: Final = title
        self.description: Final = description

    def apply(self, elements: Iterable[Task]) -> Iterable[Task]:
        if self.status:
            elements = _filter_by_status(elements, self.status)
        if self.due_date_from:
            elements = _filter_by_due_date_from(elements, self.due_date_from)
        if self.due_date_to:
            elements = _filter_by_due_date_to(elements, self.due_date_to)
        if self.title:
            elements = _filter_by_title(elements, self.title)
        if self.description:
            elements = _filter_by_description(elements, self.description)
        return elements
