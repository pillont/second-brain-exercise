from datetime import date
from typing import List

from source.models.task import Task, TaskStatus
from source.models.task_filters import TaskFilters


def _make_task(
    id: int,
    title: str = "Task",
    description: str = "Desc",
    due_date: date = date(2026, 6, 1),
    status: TaskStatus = TaskStatus.INCOMPLETE,
) -> Task:
    return Task(
        id=id,
        title=title,
        description=description,
        due_date=due_date,
        status=status,
    )


def _apply(filters: TaskFilters, tasks: List[Task]) -> List[Task]:
    return list(filters.apply(iter(tasks)))


def test_apply_no_filter_returns_all() -> None:
    tasks = [_make_task(1), _make_task(2)]

    result = _apply(TaskFilters(), tasks)

    assert result == tasks


def test_filter_by_status_complete() -> None:
    tasks = [
        _make_task(1, status=TaskStatus.INCOMPLETE),
        _make_task(2, status=TaskStatus.COMPLETE),
    ]

    result = _apply(TaskFilters(status=TaskStatus.COMPLETE), tasks)

    assert len(result) == 1
    assert result[0].id == 2


def test_filter_by_status_incomplete() -> None:
    tasks = [
        _make_task(1, status=TaskStatus.INCOMPLETE),
        _make_task(2, status=TaskStatus.COMPLETE),
    ]

    result = _apply(TaskFilters(status=TaskStatus.INCOMPLETE), tasks)

    assert len(result) == 1
    assert result[0].id == 1


def test_filter_by_due_date_from_inclusive() -> None:
    tasks = [
        _make_task(1, due_date=date(2026, 1, 1)),
        _make_task(2, due_date=date(2026, 6, 1)),
        _make_task(3, due_date=date(2026, 12, 31)),
    ]

    result = _apply(TaskFilters(due_date_from=date(2026, 6, 1)), tasks)

    assert [t.id for t in result] == [2, 3]


def test_filter_by_due_date_to_inclusive() -> None:
    tasks = [
        _make_task(1, due_date=date(2026, 1, 1)),
        _make_task(2, due_date=date(2026, 6, 1)),
        _make_task(3, due_date=date(2026, 12, 31)),
    ]

    result = _apply(TaskFilters(due_date_to=date(2026, 6, 1)), tasks)

    assert [t.id for t in result] == [1, 2]


def test_filter_by_due_date_range() -> None:
    tasks = [
        _make_task(1, due_date=date(2026, 1, 1)),
        _make_task(2, due_date=date(2026, 6, 1)),
        _make_task(3, due_date=date(2026, 12, 31)),
    ]

    result = _apply(
        TaskFilters(due_date_from=date(2026, 3, 1), due_date_to=date(2026, 9, 1)),
        tasks,
    )

    assert [t.id for t in result] == [2]


def test_filter_by_title_case_insensitive() -> None:
    tasks = [
        _make_task(1, title="Buy Milk"),
        _make_task(2, title="walk the dog"),
        _make_task(3, title="buy groceries"),
    ]

    result = _apply(TaskFilters(title="buy"), tasks)

    assert [t.id for t in result] == [1, 3]


def test_filter_by_description_case_insensitive() -> None:
    tasks = [
        _make_task(1, description="At the Store"),
        _make_task(2, description="in the park"),
        _make_task(3, description="at home"),
    ]

    result = _apply(TaskFilters(description="at"), tasks)

    assert [t.id for t in result] == [1, 3]


def test_filter_combined_status_and_title() -> None:
    tasks = [
        _make_task(1, title="Buy milk", status=TaskStatus.INCOMPLETE),
        _make_task(2, title="Buy eggs", status=TaskStatus.COMPLETE),
        _make_task(3, title="Walk dog", status=TaskStatus.INCOMPLETE),
    ]

    result = _apply(
        TaskFilters(status=TaskStatus.INCOMPLETE, title="buy"),
        tasks,
    )

    assert [t.id for t in result] == [1]


def test_filter_returns_empty_when_no_match() -> None:
    tasks = [_make_task(1, status=TaskStatus.INCOMPLETE)]

    result = _apply(TaskFilters(status=TaskStatus.COMPLETE), tasks)

    assert result == []
