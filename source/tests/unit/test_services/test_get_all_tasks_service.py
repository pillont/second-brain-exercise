from datetime import date
from typing import Iterable, List
from unittest.mock import MagicMock
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
    mock_repo.get_all.return_value = (t for t in fake_tasks)
    service = GetAllTasksService(repository=mock_repo)

    result = list(service.get_all_tasks())

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
    mock_repo.get_all.return_value = (task for task in [task1, task2])
    service = GetAllTasksService(repository=mock_repo)

    result = list(service.get_all_tasks())

    assert len(result) == 2
    assert result[0] is task1
    assert result[1] is task2


def test_get_all_tasks_propagates_repository_error() -> None:
    mock_repo = MagicMock()
    mock_repo.get_all.side_effect = RuntimeError("Database error")
    service = GetAllTasksService(repository=mock_repo)

    try:
        service.get_all_tasks()
        assert False, "Expected RuntimeError to be raised"
    except RuntimeError as e:
        assert str(e) == "Database error"
