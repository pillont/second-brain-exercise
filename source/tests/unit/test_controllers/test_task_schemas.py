from datetime import date
from source.controllers.entities.link import Link, Links
from source.controllers.entities.task_entity import TaskDataEntity, TaskEntity
from source.controllers.schemas.task_data_schema import TaskDataSchema
from source.controllers.schemas.task_schema import TaskSchema
from source.models.task import TaskStatus


def test_task_data_schema_load_returns_entity() -> None:
    schema = TaskDataSchema()
    data = {
        "title": "Buy milk",
        "description": "At the store",
        "due_date": "2026-05-01",
    }

    result = schema.load(data)

    assert isinstance(result, TaskDataEntity)
    assert result.title == "Buy milk"
    assert result.due_date == date(2026, 5, 1)


def test_task_schema_dump_has_correct_keys() -> None:
    schema = TaskSchema()
    entity = TaskEntity(
        id=1,
        title="Buy milk",
        description="At the store",
        due_date=date(2026, 5, 1),
        status=TaskStatus.INCOMPLETE,
        links=Links(self_link=Link(href="/tasks/1")),
    )

    result = schema.dump(entity)

    assert "id" in result
    assert "title" in result
    assert "description" in result
    assert "due_date" in result
    assert "status" in result
    assert "_links" in result


def test_task_schema_dump_links_structure() -> None:
    schema = TaskSchema()
    entity = TaskEntity(
        id=1,
        title="Buy milk",
        description="At the store",
        due_date=date(2026, 5, 1),
        status=TaskStatus.INCOMPLETE,
        links=Links(self_link=Link(href="/tasks/1")),
    )

    result = schema.dump(entity)

    assert result["_links"]["self"]["href"] == "/tasks/1"
