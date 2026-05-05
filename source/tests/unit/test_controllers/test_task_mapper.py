from datetime import date

from source.controllers.v1.entities.link import HttpMethod
from source.controllers.v1.entities.task_entity import (
    TaskDataEntity,
    TaskUpdateDataEntity,
)
from source.controllers.v1.mappers.task_mapper import (
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

    assert result["links"]["self_link"]["href"] == "/v1/tasks/42"


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
    assert result["links"]["tasks"]["href"] == "/v1/tasks/"


def test_to_task_entity_sets_update_link() -> None:
    task = Task(
        id=42,
        title="Buy milk",
        description="At the store",
        due_date=date(2026, 5, 1),
        status=TaskStatus.INCOMPLETE,
    )

    result = to_task_entity(task)

    assert result["links"]["update"]["href"] == "/v1/tasks/42"
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

    assert result["links"]["delete"]["href"] == "/v1/tasks/42"
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


def _make_list_entity(
    sort_by=None,
    sort_direction=None,
):
    from source.controllers.v1.entities.tasks_list_argument_entity import (
        TasksListArgumentEntity,
    )

    return TasksListArgumentEntity(
        cursor=None,
        page_size=None,
        status=None,
        due_date_from=None,
        due_date_to=None,
        title=None,
        description=None,
        sort_by=sort_by,
        sort_direction=sort_direction,
    )


def test_to_task_sort_defaults_to_id_asc_when_no_params() -> None:
    from source.controllers.v1.mappers.task_mapper import to_task_sort
    from source.models.task_sort import SortDirection, SortField

    result = to_task_sort(_make_list_entity())

    assert result.field == SortField.ID
    assert result.direction == SortDirection.ASC


def test_to_task_sort_maps_sort_by_title() -> None:
    from source.controllers.v1.mappers.task_mapper import to_task_sort
    from source.models.task_sort import SortDirection, SortField

    result = to_task_sort(_make_list_entity(sort_by=SortField.TITLE))

    assert result.field == SortField.TITLE
    assert result.direction == SortDirection.ASC


def test_to_task_sort_maps_sort_direction_desc() -> None:
    from source.controllers.v1.mappers.task_mapper import to_task_sort
    from source.models.task_sort import SortDirection, SortField

    result = to_task_sort(_make_list_entity(sort_direction=SortDirection.DESC))

    assert result.field == SortField.ID
    assert result.direction == SortDirection.DESC


def test_to_task_sort_maps_sort_by_and_direction() -> None:
    from source.controllers.v1.mappers.task_mapper import to_task_sort
    from source.models.task_sort import SortDirection, SortField

    result = to_task_sort(
        _make_list_entity(sort_by=SortField.DUE_DATE, sort_direction=SortDirection.DESC)
    )

    assert result.field == SortField.DUE_DATE
    assert result.direction == SortDirection.DESC
