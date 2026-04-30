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


def test_get_all_returns_empty_initially() -> None:
    repo = FakeTaskRepository()

    result = list(repo.get_all())

    assert result == []


def test_get_all_returns_created_task() -> None:
    repo = FakeTaskRepository()
    task_data = TaskData(
        title="Buy milk", description="At the store", due_date=date(2026, 5, 1)
    )
    created = repo.create(task_data)

    result = list(repo.get_all())

    assert len(result) == 1
    assert result[0] is created


def test_get_all_returns_multiple_tasks_in_order() -> None:
    repo = FakeTaskRepository()
    task_data_1 = TaskData(
        title="Buy milk", description="At the store", due_date=date(2026, 5, 1)
    )
    task_data_2 = TaskData(
        title="Buy eggs", description="At the market", due_date=date(2026, 5, 2)
    )
    created_1 = repo.create(task_data_1)
    created_2 = repo.create(task_data_2)

    result = list(repo.get_all())

    assert len(result) == 2
    assert result[0] is created_1
    assert result[1] is created_2


def test_get_all_returns_generator() -> None:
    repo = FakeTaskRepository()
    task_data = TaskData(
        title="Buy milk", description="At the store", due_date=date(2026, 5, 1)
    )
    repo.create(task_data)

    result = repo.get_all()

    assert hasattr(result, "__iter__")
    assert hasattr(result, "__next__")


def test_get_all_does_not_modify_internal_state() -> None:
    repo = FakeTaskRepository()
    task_data = TaskData(
        title="Buy milk", description="At the store", due_date=date(2026, 5, 1)
    )
    repo.create(task_data)

    list(repo.get_all())
    result = list(repo.get_all())

    assert len(result) == 1
