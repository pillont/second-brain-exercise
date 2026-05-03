from datetime import date
from typing import List

from source.models.task import Task, TaskStatus
from source.models.task_sort import SortDirection, SortField, TaskSort


def _make_task(
    id: int,
    title: str = "Task",
    due_date: date = date(2026, 6, 1),
    status: TaskStatus = TaskStatus.INCOMPLETE,
) -> Task:
    return Task(
        id=id,
        title=title,
        description="Desc",
        due_date=due_date,
        status=status,
    )


def _apply(sort: TaskSort, tasks: List[Task]) -> List[Task]:
    return sort.apply(iter(tasks))


def test_apply_sort_by_id_asc_returns_tasks_in_id_order() -> None:
    tasks = [_make_task(3), _make_task(1), _make_task(2)]

    result = _apply(TaskSort(field=SortField.ID, direction=SortDirection.ASC), tasks)

    assert [t.id for t in result] == [1, 2, 3]


def test_apply_sort_by_id_desc_returns_tasks_in_reverse_id_order() -> None:
    tasks = [_make_task(1), _make_task(3), _make_task(2)]

    result = _apply(TaskSort(field=SortField.ID, direction=SortDirection.DESC), tasks)

    assert [t.id for t in result] == [3, 2, 1]


def test_apply_sort_by_title_asc_returns_alphabetical_order() -> None:
    tasks = [
        _make_task(1, title="Cherry"),
        _make_task(2, title="Apple"),
        _make_task(3, title="Banana"),
    ]

    result = _apply(TaskSort(field=SortField.TITLE, direction=SortDirection.ASC), tasks)

    assert [t.title for t in result] == ["Apple", "Banana", "Cherry"]


def test_apply_sort_by_title_desc_returns_reverse_alphabetical_order() -> None:
    tasks = [
        _make_task(1, title="Apple"),
        _make_task(2, title="Cherry"),
        _make_task(3, title="Banana"),
    ]

    result = _apply(
        TaskSort(field=SortField.TITLE, direction=SortDirection.DESC), tasks
    )

    assert [t.title for t in result] == ["Cherry", "Banana", "Apple"]


def test_apply_sort_by_title_asc_is_case_insensitive() -> None:
    tasks = [
        _make_task(1, title="banana"),
        _make_task(2, title="Apple"),
        _make_task(3, title="CHERRY"),
    ]

    result = _apply(TaskSort(field=SortField.TITLE, direction=SortDirection.ASC), tasks)

    assert [t.title for t in result] == ["Apple", "banana", "CHERRY"]


def test_apply_sort_by_due_date_asc_returns_earliest_first() -> None:
    tasks = [
        _make_task(1, due_date=date(2026, 12, 31)),
        _make_task(2, due_date=date(2026, 1, 1)),
        _make_task(3, due_date=date(2026, 6, 1)),
    ]

    result = _apply(
        TaskSort(field=SortField.DUE_DATE, direction=SortDirection.ASC), tasks
    )

    assert [t.id for t in result] == [2, 3, 1]


def test_apply_sort_by_due_date_desc_returns_latest_first() -> None:
    tasks = [
        _make_task(1, due_date=date(2026, 1, 1)),
        _make_task(2, due_date=date(2026, 12, 31)),
        _make_task(3, due_date=date(2026, 6, 1)),
    ]

    result = _apply(
        TaskSort(field=SortField.DUE_DATE, direction=SortDirection.DESC), tasks
    )

    assert [t.id for t in result] == [2, 3, 1]


def test_apply_sort_by_status_asc_returns_complete_before_incomplete() -> None:
    tasks = [
        _make_task(1, status=TaskStatus.INCOMPLETE),
        _make_task(2, status=TaskStatus.COMPLETE),
        _make_task(3, status=TaskStatus.INCOMPLETE),
    ]

    result = _apply(
        TaskSort(field=SortField.STATUS, direction=SortDirection.ASC), tasks
    )

    assert result[0].status == TaskStatus.COMPLETE
    assert result[1].status == TaskStatus.INCOMPLETE
    assert result[2].status == TaskStatus.INCOMPLETE


def test_apply_sort_by_status_desc_returns_incomplete_before_complete() -> None:
    tasks = [
        _make_task(1, status=TaskStatus.COMPLETE),
        _make_task(2, status=TaskStatus.INCOMPLETE),
    ]

    result = _apply(
        TaskSort(field=SortField.STATUS, direction=SortDirection.DESC), tasks
    )

    assert result[0].status == TaskStatus.INCOMPLETE
    assert result[1].status == TaskStatus.COMPLETE


def test_apply_returns_list_not_generator() -> None:
    tasks = [_make_task(1), _make_task(2)]

    result = _apply(TaskSort(), tasks)

    assert isinstance(result, list)


def test_apply_with_empty_list_returns_empty_list() -> None:
    result = _apply(TaskSort(), [])

    assert result == []


def test_apply_with_single_element_returns_single_element() -> None:
    tasks = [_make_task(1, title="Solo")]

    result = _apply(TaskSort(field=SortField.TITLE), tasks)

    assert len(result) == 1
    assert result[0].title == "Solo"


def test_apply_does_not_modify_input_list() -> None:
    tasks = [_make_task(3), _make_task(1), _make_task(2)]
    original_order = [t.id for t in tasks]

    _apply(TaskSort(field=SortField.ID, direction=SortDirection.ASC), tasks)

    assert [t.id for t in tasks] == original_order
