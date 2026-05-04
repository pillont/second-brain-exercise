from datetime import date
from typing import Iterable

from source.models.task import Task, TaskStatus
from source.models.task_filters import TaskFilters


def _filter_by_status(elements: Iterable[Task], status: TaskStatus) -> Iterable[Task]:
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


def filter_tasks_list(elements: Iterable[Task], filter: TaskFilters) -> Iterable[Task]:
    if filter.status:
        elements = _filter_by_status(elements, filter.status)

    if filter.due_date_from:
        elements = _filter_by_due_date_from(elements, filter.due_date_from)

    if filter.due_date_to:
        elements = _filter_by_due_date_to(elements, filter.due_date_to)

    if filter.title:
        elements = _filter_by_title(elements, filter.title)

    return elements
