from datetime import date
from itertools import chain
from typing import Iterable, List
from unittest.mock import MagicMock
from source.models.filtered_list import FilteredList
from source.models.task import Task, TaskStatus
from source.services.get_all_tasks_service import GetAllTasksService


def test_get_all_tasks_calls_repository() -> None:
    mock_repo = MagicMock()
    mock_repo.get_all.return_value = (
        Task(
            id=1,
            title="Buy milk",
            description="At the store",
            due_date=date(2026, 5, 1),
            status=TaskStatus.INCOMPLETE,
        )
        for _ in []
    )
    service = GetAllTasksService(repository=mock_repo)

    service.get_all_tasks()

    mock_repo.get_all.assert_called_once()


def test_get_all_tasks_returns_iterable() -> None:
    mock_repo = MagicMock()
    mock_repo.get_all.return_value = (
        Task(
            id=1,
            title="Buy milk",
            description="At the store",
            due_date=date(2026, 5, 1),
            status=TaskStatus.INCOMPLETE,
        )
        for _ in []
    )
    service = GetAllTasksService(repository=mock_repo)

    result = service.get_all_tasks()

    assert isinstance(result, Iterable)


def test_get_all_tasks_returns_empty_when_no_tasks() -> None:
    mock_repo = MagicMock()
    fake_tasks: List[Task] = []
    mock_repo.get_all.return_value = FilteredList((t for t in fake_tasks), False)
    service = GetAllTasksService(repository=mock_repo)

    result = list(service.get_all_tasks().elements)

    assert result == []


def test_get_all_tasks_returns_multiple_tasks() -> None:
    mock_repo = MagicMock()
    task1 = Task(
        id=1,
        title="Buy milk",
        description="At the store",
        due_date=date(2026, 5, 1),
        status=TaskStatus.INCOMPLETE,
    )
    task2 = Task(
        id=2,
        title="Buy eggs",
        description="At the market",
        due_date=date(2026, 5, 2),
        status=TaskStatus.INCOMPLETE,
    )
    mock_repo.get_all.return_value = FilteredList(chain([task1, task2]), False)
    service = GetAllTasksService(repository=mock_repo)

    result = list(service.get_all_tasks().elements)

    assert len(result) == 2
    assert result[0] is task1
    assert result[1] is task2


def test_get_all_tasks_passes_filters_to_repository() -> None:
    from source.models.task_filters import TaskFilters
    from source.models.task import TaskStatus

    mock_repo = MagicMock()
    mock_repo.get_all.return_value = FilteredList(iter([]), False)
    service = GetAllTasksService(repository=mock_repo)
    filters = TaskFilters(status=TaskStatus.COMPLETE)

    service.get_all_tasks(filters=filters)

    mock_repo.get_all.assert_called_once_with(filters, None, None, None)


def test_get_all_tasks_passes_cursor_and_page_size_to_repository() -> None:
    mock_repo = MagicMock()
    mock_repo.get_all.return_value = FilteredList(iter([]), False)
    service = GetAllTasksService(repository=mock_repo)

    service.get_all_tasks(cursor=5, page_size=10)

    mock_repo.get_all.assert_called_once_with(None, None, 5, 10)


def test_get_all_tasks_passes_all_params_to_repository() -> None:
    from source.models.task_filters import TaskFilters
    from source.models.task import TaskStatus

    mock_repo = MagicMock()
    mock_repo.get_all.return_value = FilteredList(iter([]), False)
    service = GetAllTasksService(repository=mock_repo)
    filters = TaskFilters(status=TaskStatus.INCOMPLETE)

    service.get_all_tasks(filters=filters, cursor=3, page_size=5)

    mock_repo.get_all.assert_called_once_with(filters, None, 3, 5)


def test_get_all_tasks_propagates_repository_error() -> None:
    mock_repo = MagicMock()
    mock_repo.get_all.side_effect = RuntimeError("Database error")
    service = GetAllTasksService(repository=mock_repo)

    try:
        service.get_all_tasks()
        assert False, "Expected RuntimeError to be raised"
    except RuntimeError as e:
        assert str(e) == "Database error"


def test_get_all_tasks_passes_sort_to_repository() -> None:
    from source.models.task_sort import TaskSort, SortField

    mock_repo = MagicMock()
    mock_repo.get_all.return_value = FilteredList(iter([]), False)
    service = GetAllTasksService(repository=mock_repo)
    sort = TaskSort(field=SortField.TITLE)

    service.get_all_tasks(sort=sort)

    mock_repo.get_all.assert_called_once_with(None, sort, None, None)


def test_get_all_tasks_passes_all_params_including_sort_to_repository() -> None:
    from source.models.task_filters import TaskFilters
    from source.models.task_sort import TaskSort, SortField, SortDirection
    from source.models.task import TaskStatus

    mock_repo = MagicMock()
    mock_repo.get_all.return_value = FilteredList(iter([]), False)
    service = GetAllTasksService(repository=mock_repo)
    filters = TaskFilters(status=TaskStatus.INCOMPLETE)
    sort = TaskSort(field=SortField.TITLE, direction=SortDirection.DESC)

    service.get_all_tasks(filters=filters, sort=sort, cursor=2, page_size=5)

    mock_repo.get_all.assert_called_once_with(filters, sort, 2, 5)
