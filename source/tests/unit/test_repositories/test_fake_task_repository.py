from datetime import date
from source.models.task import Task, TaskData, TaskStatus, TaskUpdateData
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

    result = list(repo.get_all().elements)

    assert result == []


def test_get_all_returns_created_task() -> None:
    repo = FakeTaskRepository()
    task_data = TaskData(
        title="Buy milk", description="At the store", due_date=date(2026, 5, 1)
    )
    created = repo.create(task_data)

    result = list(repo.get_all().elements)

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

    result = list(repo.get_all().elements)

    assert len(result) == 2
    assert result[0] is created_1
    assert result[1] is created_2


def test_get_all_returns_iterable() -> None:
    repo = FakeTaskRepository()
    task_data = TaskData(
        title="Buy milk", description="At the store", due_date=date(2026, 5, 1)
    )
    repo.create(task_data)

    result = repo.get_all().elements

    assert hasattr(result, "__iter__")
    assert hasattr(result, "__next__")


def test_get_all_returns_all_values_by_default() -> None:
    repo = FakeTaskRepository()

    for i in range(10):
        repo.create(
            TaskData(
                title=f"element1{i}",
                description="At the store",
                due_date=date(2026, 5, 1),
            )
        )

    result = [t for t in repo.get_all().elements]

    assert len(result) == 10


def test_get_all_returns_has_next_false_if_returns_all_values_by_default() -> None:
    repo = FakeTaskRepository()

    for i in range(10):
        repo.create(
            TaskData(
                title=f"element1{i}",
                description="At the store",
                due_date=date(2026, 5, 1),
            )
        )

    result = repo.get_all()
    assert not result.has_next


def test_get_all_returns_has_next_false_if_returns_all_values() -> None:
    repo = FakeTaskRepository()

    for i in range(10):
        repo.create(
            TaskData(
                title=f"element1{i}",
                description="At the store",
                due_date=date(2026, 5, 1),
            )
        )

    result = repo.get_all(page_size=10)
    assert not result.has_next

    result = repo.get_all(cursor=6, page_size=4)
    assert not result.has_next


def test_get_all_returns_has_next_true_if_not_returns_all_values() -> None:
    repo = FakeTaskRepository()

    for i in range(10):
        repo.create(
            TaskData(
                title=f"element1{i}",
                description="At the store",
                due_date=date(2026, 5, 1),
            )
        )

    result = repo.get_all(page_size=8)
    assert result.has_next

    result = repo.get_all(cursor=2, page_size=2)
    assert result.has_next


def test_get_all_returns_firsts_elements_if_element_size_is_defined() -> None:
    repo = FakeTaskRepository()

    for i in range(10):
        repo.create(
            TaskData(
                title=f"element1{i}",
                description="At the store",
                due_date=date(2026, 5, 1),
            )
        )

    result = [t for t in repo.get_all(page_size=4).elements]

    assert len(result) == 4
    assert result[0].id == 1
    assert result[1].id == 2
    assert result[2].id == 3
    assert result[3].id == 4


def test_get_all_returns_firsts_elements_if_page_size_and_cursor_is_defined() -> None:
    repo = FakeTaskRepository()

    for i in range(10):
        repo.create(
            TaskData(
                title=f"element1{i}",
                description="At the store",
                due_date=date(2026, 5, 1),
            )
        )

    result = [t for t in repo.get_all(page_size=4, cursor=4).elements]

    assert len(result) == 4
    assert result[0].id == 5
    assert result[1].id == 6
    assert result[2].id == 7
    assert result[3].id == 8


def test_get_all_returns_firsts_elements_if_cursor_is_defined() -> None:
    repo = FakeTaskRepository()

    for i in range(10):
        repo.create(
            TaskData(
                title=f"element1{i}",
                description="At the store",
                due_date=date(2026, 5, 1),
            )
        )

    result = [t for t in repo.get_all(cursor=4).elements]

    assert len(result) == 6
    assert result[0].id == 5
    assert result[1].id == 6
    assert result[2].id == 7
    assert result[3].id == 8
    assert result[4].id == 9
    assert result[5].id == 10


def test_get_all_does_not_modify_internal_state() -> None:
    repo = FakeTaskRepository()
    task_data = TaskData(
        title="Buy milk", description="At the store", due_date=date(2026, 5, 1)
    )
    repo.create(task_data)

    list(repo.get_all().elements)
    result = list(repo.get_all().elements)

    assert len(result) == 1


def test_get_task_returns_task_by_id() -> None:
    repo = FakeTaskRepository()
    task_data = TaskData(
        title="Buy milk", description="At the store", due_date=date(2026, 5, 1)
    )
    created = repo.create(task_data)

    result = repo.get_task(created.id)

    assert result is created


def test_get_task_returns_correct_task_among_multiple() -> None:
    repo = FakeTaskRepository()
    repo.create(
        TaskData(
            title="Buy milk", description="At the store", due_date=date(2026, 5, 1)
        )
    )
    created_2 = repo.create(
        TaskData(
            title="Buy eggs", description="At the market", due_date=date(2026, 5, 2)
        )
    )

    result = repo.get_task(created_2.id)

    assert result is created_2


def test_get_task_raises_not_found_error_when_id_does_not_exist() -> None:
    from source.models.not_found_error import NotFoundError

    repo = FakeTaskRepository()

    try:
        repo.get_task(99)
        assert False, "Expected NotFoundError to be raised"
    except NotFoundError:
        pass


def test_get_task_raises_not_found_error_after_all_tasks_consumed() -> None:
    from source.models.not_found_error import NotFoundError

    repo = FakeTaskRepository()
    task_data = TaskData(
        title="Buy milk", description="At the store", due_date=date(2026, 5, 1)
    )
    repo.create(task_data)

    try:
        repo.get_task(999)
        assert False, "Expected NotFoundError to be raised"
    except NotFoundError:
        pass


def test_update_task_updates_fields() -> None:
    repo = FakeTaskRepository()
    created = repo.create(
        TaskData(
            title="Buy milk", description="At the store", due_date=date(2026, 5, 1)
        )
    )
    update_data = TaskUpdateData(
        title="Buy eggs",
        description="At the market",
        due_date=date(2026, 6, 1),
        status=TaskStatus.COMPLETE,
    )

    repo.update(created.id, update_data)

    updated = repo.get_task(created.id)
    assert updated.title == "Buy eggs"
    assert updated.description == "At the market"
    assert updated.due_date == date(2026, 6, 1)
    assert updated.status == TaskStatus.COMPLETE


def test_update_task_raises_not_found_error_for_unknown_id() -> None:
    from source.models.not_found_error import NotFoundError

    repo = FakeTaskRepository()
    update_data = TaskUpdateData(
        title="Buy eggs",
        description="At the market",
        due_date=date(2026, 6, 1),
        status=TaskStatus.COMPLETE,
    )

    try:
        repo.update(99, update_data)
        assert False, "Expected NotFoundError to be raised"
    except NotFoundError:
        pass
