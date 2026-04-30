from datetime import date
from unittest.mock import MagicMock

from source.models.not_found_error import NotFoundError
from source.models.task import TaskStatus, TaskUpdateData
from source.services.update_task_service import UpdateTaskService


def test_update_task_calls_repository() -> None:
    mock_repo = MagicMock()
    service = UpdateTaskService(repository=mock_repo)
    task_update_data = TaskUpdateData(
        title="Updated",
        description="New desc",
        due_date=date(2026, 5, 1),
        status=TaskStatus.COMPLETE,
    )

    service.update_task(1, task_update_data)

    mock_repo.update.assert_called_once_with(1, task_update_data)


def test_update_task_propagates_not_found_error() -> None:
    mock_repo = MagicMock()
    mock_repo.update.side_effect = NotFoundError()
    service = UpdateTaskService(repository=mock_repo)
    task_update_data = TaskUpdateData(
        title="Updated",
        description="New desc",
        due_date=date(2026, 5, 1),
        status=TaskStatus.COMPLETE,
    )

    try:
        service.update_task(99, task_update_data)
        assert False, "Expected NotFoundError to be raised"
    except NotFoundError:
        pass
