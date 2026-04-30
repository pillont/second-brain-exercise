from datetime import date
from unittest.mock import MagicMock
from source.models.task import Task, TaskData, TaskStatus
from source.services.task_service import CreateTaskService


def test_create_task_calls_repository() -> None:
    mock_repo = MagicMock()
    task_data = TaskData(
        title="Buy milk", description="At the store", due_date=date(2026, 5, 1)
    )
    mock_repo.create.return_value = Task(
        id=1,
        title="Buy milk",
        description="At the store",
        due_date=date(2026, 5, 1),
        status=TaskStatus.INCOMPLETE,
    )
    service = CreateTaskService(repository=mock_repo)

    service.create_task(task_data)

    mock_repo.create.assert_called_once_with(task_data)


def test_create_task_returns_result() -> None:
    mock_repo = MagicMock()
    task_data = TaskData(
        title="Buy milk", description="At the store", due_date=date(2026, 5, 1)
    )
    expected = Task(
        id=1,
        title="Buy milk",
        description="At the store",
        due_date=date(2026, 5, 1),
        status=TaskStatus.INCOMPLETE,
    )
    mock_repo.create.return_value = expected
    service = CreateTaskService(repository=mock_repo)

    result = service.create_task(task_data)

    assert result is expected
