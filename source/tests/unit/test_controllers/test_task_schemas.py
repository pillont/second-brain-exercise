from datetime import date

from marshmallow import ValidationError

from source.controllers.v1.entities.link import HttpMethod, LinkEntity
from source.controllers.v1.entities.task_entity import TaskEntity, TaskLinks
from source.controllers.v1.schemas.task_data_schema import TaskDataSchema
from source.controllers.v1.schemas.task_schema import TaskSchema
from source.controllers.v1.schemas.task_update_data_schema import TaskUpdateDataSchema
from source.models.task import TaskStatus


def test_task_data_schema_load_returns_entity() -> None:
    schema = TaskDataSchema()
    data = {
        "title": "Buy milk",
        "description": "At the store",
        "due_date": "2026-05-01",
    }

    result = schema.load(data)

    assert isinstance(result, dict)
    assert result["title"] == "Buy milk"
    assert result["due_date"] == date(2026, 5, 1)


def test_task_schema_dump_has_correct_keys() -> None:
    schema = TaskSchema()
    entity = TaskEntity(
        id=1,
        title="Buy milk",
        description="At the store",
        due_date=date(2026, 5, 1),
        status=TaskStatus.INCOMPLETE,
        links=TaskLinks(
            self_link=LinkEntity(href="/v1/tasks/1"),
            tasks=LinkEntity(href="/v1/tasks/"),
            update=LinkEntity(href="/v1/tasks/1", type=HttpMethod.PUT),
            delete=LinkEntity(href="/v1/tasks/1", type=HttpMethod.DELETE),
        ),
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
        links=TaskLinks(
            self_link=LinkEntity(href="/v1/tasks/1"),
            tasks=LinkEntity(href="/v1/tasks/"),
            update=LinkEntity(href="/v1/tasks/1", type=HttpMethod.PUT),
            delete=LinkEntity(href="/v1/tasks/1", type=HttpMethod.DELETE),
        ),
    )

    result = schema.dump(entity)

    assert result["_links"]["self"]["href"] == "/v1/tasks/1"


def test_task_schema_dump_links_includes_tasks() -> None:
    schema = TaskSchema()
    entity = TaskEntity(
        id=1,
        title="Buy milk",
        description="At the store",
        due_date=date(2026, 5, 1),
        status=TaskStatus.INCOMPLETE,
        links=TaskLinks(
            self_link=LinkEntity(href="/v1/tasks/1"),
            tasks=LinkEntity(href="/v1/tasks/"),
            update=LinkEntity(href="/v1/tasks/1", type=HttpMethod.PUT),
            delete=LinkEntity(href="/v1/tasks/1", type=HttpMethod.DELETE),
        ),
    )

    result = schema.dump(entity)

    assert result["_links"]["tasks"]["href"] == "/v1/tasks/"


def test_task_schema_with_many_true_dumps_list() -> None:
    schema = TaskSchema(many=True)
    entity1 = TaskEntity(
        id=1,
        title="Buy milk",
        description="At the store",
        due_date=date(2026, 5, 1),
        status=TaskStatus.INCOMPLETE,
        links=TaskLinks(
            self_link=LinkEntity(href="/v1/tasks/1"),
            tasks=LinkEntity(href="/v1/tasks/"),
            update=LinkEntity(href="/v1/tasks/1", type=HttpMethod.PUT),
            delete=LinkEntity(href="/v1/tasks/1", type=HttpMethod.DELETE),
        ),
    )
    entity2 = TaskEntity(
        id=2,
        title="Buy eggs",
        description="At the market",
        due_date=date(2026, 5, 2),
        status=TaskStatus.INCOMPLETE,
        links=TaskLinks(
            self_link=LinkEntity(href="/v1/tasks/2"),
            tasks=LinkEntity(href="/v1/tasks/"),
            update=LinkEntity(href="/v1/tasks/2", type=HttpMethod.PUT),
            delete=LinkEntity(href="/v1/tasks/2", type=HttpMethod.DELETE),
        ),
    )

    result = schema.dump([entity1, entity2])

    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0]["id"] == 1
    assert result[1]["id"] == 2


def test_task_schema_with_many_true_dumps_empty_list() -> None:
    schema = TaskSchema(many=True)

    result = schema.dump([])

    assert isinstance(result, list)
    assert len(result) == 0


def test_task_schema_with_many_true_includes_links_per_entity() -> None:
    schema = TaskSchema(many=True)
    entity1 = TaskEntity(
        id=1,
        title="Buy milk",
        description="At the store",
        due_date=date(2026, 5, 1),
        status=TaskStatus.INCOMPLETE,
        links=TaskLinks(
            self_link=LinkEntity(href="/v1/tasks/1"),
            tasks=LinkEntity(href="/v1/tasks/"),
            update=LinkEntity(href="/v1/tasks/1", type=HttpMethod.PUT),
            delete=LinkEntity(href="/v1/tasks/1", type=HttpMethod.DELETE),
        ),
    )
    entity2 = TaskEntity(
        id=2,
        title="Buy eggs",
        description="At the market",
        due_date=date(2026, 5, 2),
        status=TaskStatus.INCOMPLETE,
        links=TaskLinks(
            self_link=LinkEntity(href="/v1/tasks/2"),
            tasks=LinkEntity(href="/v1/tasks/"),
            update=LinkEntity(href="/v1/tasks/2", type=HttpMethod.PUT),
            delete=LinkEntity(href="/v1/tasks/2", type=HttpMethod.DELETE),
        ),
    )

    result = schema.dump([entity1, entity2])

    assert result[0]["_links"]["self"]["href"] == "/v1/tasks/1"
    assert result[1]["_links"]["self"]["href"] == "/v1/tasks/2"


def test_task_update_data_schema_loads_valid_data() -> None:
    schema = TaskUpdateDataSchema()
    data = {
        "title": "Buy milk",
        "description": "At the store",
        "due_date": "2026-05-01",
        "status": "Complete",
    }

    result = schema.load(data)

    assert isinstance(result, dict)
    assert result["title"] == "Buy milk"
    assert result["due_date"] == date(2026, 5, 1)
    assert result["status"] == "Complete"


def test_task_update_data_schema_loads_invalid_status() -> None:
    schema = TaskUpdateDataSchema()
    data = {
        "title": "Buy milk",
        "description": "At the store",
        "due_date": "2026-05-01",
        "status": "UNKNOWN STATUS !",
    }

    try:
        schema.load(data)
        assert False, "Expected ValidationError to be raised"
    except ValidationError:
        pass


def test_task_update_data_schema_missing_status_raises_error() -> None:

    schema = TaskUpdateDataSchema()
    data = {
        "title": "Buy milk",
        "description": "At the store",
        "due_date": "2026-05-01",
    }

    try:
        schema.load(data)
        assert False, "Expected ValidationError to be raised"
    except ValidationError:
        pass
