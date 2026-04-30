from datetime import date
from unittest.mock import MagicMock
from source.models.task import Task, TaskStatus
from source.models.not_found_error import NotFoundError
from source.services.get_task_service import GetTaskService


def test_get_task_calls_repository_with_id() -> None:
    mock_repo = MagicMock()
    mock_repo.get_task.return_value = Task(
        id=1,
        title="Buy milk",
        description="At the store",
        due_date=date(2026, 5, 1),
        status=TaskStatus.INCOMPLETE,
    )
    service = GetTaskService(repository=mock_repo)

    service.get_task(1)

    mock_repo.get_task.assert_called_once_with(1)


def test_get_task_returns_task() -> None:
    mock_repo = MagicMock()
    expected = Task(
        id=1,
        title="Buy milk",
        description="At the store",
        due_date=date(2026, 5, 1),
        status=TaskStatus.INCOMPLETE,
    )
    mock_repo.get_task.return_value = expected
    service = GetTaskService(repository=mock_repo)

    result = service.get_task(1)

    assert result is expected


def test_get_task_propagates_not_found_error() -> None:
    mock_repo = MagicMock()
    mock_repo.get_task.side_effect = NotFoundError()
    service = GetTaskService(repository=mock_repo)

    try:
        service.get_task(99)
        assert False, "Expected NotFoundError to be raised"
    except NotFoundError:
        pass


def test_get_task_propagates_repository_error() -> None:
    mock_repo = MagicMock()
    mock_repo.get_task.side_effect = RuntimeError("Database error")
    service = GetTaskService(repository=mock_repo)

    try:
        service.get_task(1)
        assert False, "Expected RuntimeError to be raised"
    except RuntimeError as e:
        assert str(e) == "Database error"
