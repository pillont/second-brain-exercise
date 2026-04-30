from datetime import date
from source.models.task import Task, TaskData, TaskStatus
from source.controllers.entities.task_entity import TaskDataEntity, TaskEntity
from source.controllers.mappers.task_mapper import to_task_data, to_task_entity


def test_to_task_data_maps_fields() -> None:
    entity = TaskDataEntity(
        title="Buy milk", description="At the store", due_date=date(2026, 5, 1)
    )

    result = to_task_data(entity)

    assert isinstance(result, TaskData)
    assert result.title == "Buy milk"
    assert result.description == "At the store"
    assert result.due_date == date(2026, 5, 1)


def test_to_task_entity_maps_fields() -> None:
    task = Task(
        id=1,
        title="Buy milk",
        description="At the store",
        due_date=date(2026, 5, 1),
        status=TaskStatus.INCOMPLETE,
    )

    result = to_task_entity(task)

    assert isinstance(result, TaskEntity)
    assert result.id == 1
    assert result.title == "Buy milk"
    assert result.description == "At the store"
    assert result.due_date == date(2026, 5, 1)
    assert result.status == TaskStatus.INCOMPLETE


def test_to_task_entity_sets_self_link() -> None:
    task = Task(
        id=42,
        title="Buy milk",
        description="At the store",
        due_date=date(2026, 5, 1),
        status=TaskStatus.INCOMPLETE,
    )

    result = to_task_entity(task)

    assert result.links.self_link.href == "/tasks/42"
