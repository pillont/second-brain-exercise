from datetime import date
from source.models.task import Task, TaskData, TaskStatus
from source.repositories.fake_task_repository import FakeTaskRepository


def test_create_returns_task() -> None:
    repo = FakeTaskRepository()
    task_data = TaskData(
        title="Buy milk", description="At the store", due_date=date(2026, 5, 1)
    )

    result = repo.create(task_data)

    assert isinstance(result, Task)


def test_create_assigns_id_starting_at_one() -> None:
    repo = FakeTaskRepository()
    task_data = TaskData(
        title="Buy milk", description="At the store", due_date=date(2026, 5, 1)
    )

    result = repo.create(task_data)

    assert result.id == 1


def test_create_increments_id() -> None:
    repo = FakeTaskRepository()
    task_data = TaskData(
        title="Buy milk", description="At the store", due_date=date(2026, 5, 1)
    )

    first = repo.create(task_data)
    second = repo.create(task_data)

    assert first.id == 1
    assert second.id == 2


def test_create_sets_status_incomplete() -> None:
    repo = FakeTaskRepository()
    task_data = TaskData(
        title="Buy milk", description="At the store", due_date=date(2026, 5, 1)
    )

    result = repo.create(task_data)

    assert result.status == TaskStatus.INCOMPLETE


def test_create_stores_task_data() -> None:
    repo = FakeTaskRepository()
    task_data = TaskData(
        title="Buy milk", description="At the store", due_date=date(2026, 5, 1)
    )

    result = repo.create(task_data)

    assert result.title == "Buy milk"
    assert result.description == "At the store"
    assert result.due_date == date(2026, 5, 1)
