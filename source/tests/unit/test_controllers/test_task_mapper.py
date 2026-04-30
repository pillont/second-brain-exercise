from datetime import date
from source.controllers.entities.link import HttpMethod
from source.controllers.entities.task_entity import (
    TaskDataEntity,
    TaskUpdateDataEntity,
)
from source.controllers.mappers.task_mapper import (
    to_task_data,
    to_task_entity,
    to_task_update_data,
)
from source.models.task import Task, TaskData, TaskStatus, TaskUpdateData


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

    assert isinstance(result, dict)
    assert result["id"] == 1
    assert result["title"] == "Buy milk"
    assert result["description"] == "At the store"
    assert result["due_date"] == date(2026, 5, 1)
    assert result["status"] == TaskStatus.INCOMPLETE


def test_to_task_entity_sets_self_link() -> None:
    task = Task(
        id=42,
        title="Buy milk",
        description="At the store",
        due_date=date(2026, 5, 1),
        status=TaskStatus.INCOMPLETE,
    )

    result = to_task_entity(task)

    assert result["links"]["self_link"]["href"] == "/tasks/42"


def test_to_task_entity_sets_tasks_link() -> None:
    task = Task(
        id=42,
        title="Buy milk",
        description="At the store",
        due_date=date(2026, 5, 1),
        status=TaskStatus.INCOMPLETE,
    )

    result = to_task_entity(task)

    assert isinstance(result["links"], dict)
    assert result["links"]["tasks"]["href"] == "/tasks/"


def test_to_task_entity_sets_update_link() -> None:
    task = Task(
        id=42,
        title="Buy milk",
        description="At the store",
        due_date=date(2026, 5, 1),
        status=TaskStatus.INCOMPLETE,
    )

    result = to_task_entity(task)

    assert result["links"]["update"]["href"] == "/tasks/42"
    assert result["links"]["update"]["type"] == HttpMethod.PUT


def test_to_task_entity_sets_delete_link() -> None:
    task = Task(
        id=42,
        title="Buy milk",
        description="At the store",
        due_date=date(2026, 5, 1),
        status=TaskStatus.INCOMPLETE,
    )

    result = to_task_entity(task)

    assert result["links"]["delete"]["href"] == "/tasks/42"
    assert result["links"]["delete"]["type"] == HttpMethod.DELETE


def test_to_task_update_data_maps_all_fields() -> None:
    entity = TaskUpdateDataEntity(
        title="Buy eggs",
        description="At the market",
        due_date=date(2026, 6, 1),
        status=TaskStatus.COMPLETE,
    )

    result = to_task_update_data(entity)

    assert isinstance(result, TaskUpdateData)
    assert result.title == "Buy eggs"
    assert result.description == "At the market"
    assert result.due_date == date(2026, 6, 1)
    assert result.status == TaskStatus.COMPLETE
