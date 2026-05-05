from datetime import date

import pytest
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from source.models.not_found_error import NotFoundError
from source.models.task import Task, TaskData, TaskStatus, TaskUpdateData
from source.models.task_cursor import TaskCursor, decode_task_cursor
from source.models.task_filters import TaskFilters
from source.models.task_sort import SortDirection, SortField, TaskSort
from source.repositories.sqlalchemy.tasks.repositories import (
    CreateTaskSqlalchemyRepository, DeleteTaskSqlalchemyRepository,
    GetTaskSqlalchemyRepository, UpdateTaskSqlalchemyRepository)
from source.repositories.sqlalchemy.tasks.repositories.get_all import \
    GetAllTasksSqlalchemyRepository

TASK_DATA = TaskData(
    title="Buy milk", description="At the store", due_date=date(2026, 5, 1)
)
TASK_DATA_2 = TaskData(
    title="Buy eggs", description="At the market", due_date=date(2026, 5, 2)
)


@pytest.fixture
def engine(tmp_path: pytest.TempPathFactory) -> Engine:
    return create_engine("sqlite:///:memory:")


@pytest.fixture
def create_repo(engine: Engine) -> CreateTaskSqlalchemyRepository:
    return CreateTaskSqlalchemyRepository(engine)


@pytest.fixture
def get_all_repo(engine: Engine) -> GetAllTasksSqlalchemyRepository:
    return GetAllTasksSqlalchemyRepository(engine)


@pytest.fixture
def get_repo(engine: Engine) -> GetTaskSqlalchemyRepository:
    return GetTaskSqlalchemyRepository(engine)


@pytest.fixture
def update_repo(engine: Engine) -> UpdateTaskSqlalchemyRepository:
    return UpdateTaskSqlalchemyRepository(engine)


@pytest.fixture
def delete_repo(engine: Engine) -> DeleteTaskSqlalchemyRepository:
    return DeleteTaskSqlalchemyRepository(engine)


def _make_complete(
    create_repo: CreateTaskSqlalchemyRepository,
    update_repo: UpdateTaskSqlalchemyRepository,
    task_data: TaskData,
) -> Task:
    created = create_repo.create(task_data)
    update_repo.update(
        created.id,
        TaskUpdateData(
            title=created.title,
            description=created.description,
            due_date=created.due_date,
            status=TaskStatus.COMPLETE,
        ),
    )
    return created


def test_create_returns_task(create_repo: CreateTaskSqlalchemyRepository) -> None:
    result = create_repo.create(TASK_DATA)

    assert isinstance(result, Task)


def test_create_assigns_auto_incremented_id(
    create_repo: CreateTaskSqlalchemyRepository,
) -> None:
    result = create_repo.create(TASK_DATA)

    assert isinstance(result.id, int)
    assert result.id >= 1


def test_create_increments_id(create_repo: CreateTaskSqlalchemyRepository) -> None:
    first = create_repo.create(TASK_DATA)
    second = create_repo.create(TASK_DATA_2)

    assert second.id == first.id + 1


def test_create_sets_status_incomplete(
    create_repo: CreateTaskSqlalchemyRepository,
) -> None:
    result = create_repo.create(TASK_DATA)

    assert result.status == TaskStatus.INCOMPLETE


def test_create_stores_task_data(create_repo: CreateTaskSqlalchemyRepository) -> None:
    result = create_repo.create(TASK_DATA)

    assert result.title == TASK_DATA.title
    assert result.description == TASK_DATA.description
    assert result.due_date == TASK_DATA.due_date


def test_get_all_returns_empty_initially(
    get_all_repo: GetAllTasksSqlalchemyRepository,
) -> None:
    result = list(get_all_repo.get_all().elements)

    assert result == []


def test_get_all_returns_created_task(
    create_repo: CreateTaskSqlalchemyRepository,
    get_all_repo: GetAllTasksSqlalchemyRepository,
) -> None:
    created = create_repo.create(TASK_DATA)

    result = list(get_all_repo.get_all().elements)

    assert len(result) == 1
    assert result[0].id == created.id
    assert result[0].title == created.title


def test_get_all_returns_multiple_tasks(
    create_repo: CreateTaskSqlalchemyRepository,
    get_all_repo: GetAllTasksSqlalchemyRepository,
) -> None:
    create_repo.create(TASK_DATA)
    create_repo.create(TASK_DATA_2)

    result = list(get_all_repo.get_all().elements)

    assert len(result) == 2


def test_get_all_has_next_false_when_all_returned(
    create_repo: CreateTaskSqlalchemyRepository,
    get_all_repo: GetAllTasksSqlalchemyRepository,
) -> None:
    for _ in range(5):
        create_repo.create(TASK_DATA)

    assert get_all_repo.get_all().has_next is False
    assert get_all_repo.get_all(page_size=5).has_next is False


def test_get_all_has_next_true_when_more_available(
    create_repo: CreateTaskSqlalchemyRepository,
    get_all_repo: GetAllTasksSqlalchemyRepository,
) -> None:
    for _ in range(5):
        create_repo.create(TASK_DATA)

    assert get_all_repo.get_all(page_size=3).has_next is True


def test_get_all_returns_first_n_elements_with_page_size(
    create_repo: CreateTaskSqlalchemyRepository,
    get_all_repo: GetAllTasksSqlalchemyRepository,
) -> None:
    tasks = [create_repo.create(TASK_DATA) for _ in range(5)]

    result = list(get_all_repo.get_all(page_size=3).elements)

    assert len(result) == 3
    assert result[0].id == tasks[0].id


def test_get_all_returns_elements_after_cursor(
    create_repo: CreateTaskSqlalchemyRepository,
    get_all_repo: GetAllTasksSqlalchemyRepository,
) -> None:
    tasks = [create_repo.create(TASK_DATA) for _ in range(5)]

    result = list(
        get_all_repo.get_all(
            cursor=TaskCursor(sort_value=str(tasks[2].id), id=tasks[2].id)
        ).elements
    )

    assert len(result) == 2
    assert result[0].id == tasks[3].id
    assert result[1].id == tasks[4].id


def test_get_all_cursor_and_page_size(
    create_repo: CreateTaskSqlalchemyRepository,
    get_all_repo: GetAllTasksSqlalchemyRepository,
) -> None:
    tasks = [create_repo.create(TASK_DATA) for _ in range(6)]

    result = list(
        get_all_repo.get_all(
            cursor=TaskCursor(sort_value=str(tasks[1].id), id=tasks[1].id), page_size=2
        ).elements
    )

    assert len(result) == 2
    assert result[0].id == tasks[2].id
    assert result[1].id == tasks[3].id


def test_get_all_filter_by_status(
    create_repo: CreateTaskSqlalchemyRepository,
    get_all_repo: GetAllTasksSqlalchemyRepository,
    update_repo: UpdateTaskSqlalchemyRepository,
) -> None:
    _make_complete(create_repo, update_repo, TASK_DATA)
    create_repo.create(TASK_DATA_2)

    result = list(
        get_all_repo.get_all(filters=TaskFilters(status=TaskStatus.COMPLETE)).elements
    )

    assert len(result) == 1
    assert result[0].status == TaskStatus.COMPLETE


def test_get_all_filter_by_status_excludes_non_matching(
    create_repo: CreateTaskSqlalchemyRepository,
    get_all_repo: GetAllTasksSqlalchemyRepository,
    update_repo: UpdateTaskSqlalchemyRepository,
) -> None:
    _make_complete(create_repo, update_repo, TASK_DATA)
    create_repo.create(TASK_DATA_2)

    result = list(
        get_all_repo.get_all(filters=TaskFilters(status=TaskStatus.INCOMPLETE)).elements
    )

    assert len(result) == 1
    assert result[0].status == TaskStatus.INCOMPLETE


def test_get_all_filter_by_due_date_from(
    create_repo: CreateTaskSqlalchemyRepository,
    get_all_repo: GetAllTasksSqlalchemyRepository,
) -> None:
    create_repo.create(TaskData(title="T1", description="D", due_date=date(2026, 1, 1)))
    create_repo.create(
        TaskData(title="T2", description="D", due_date=date(2026, 12, 31))
    )

    result = list(
        get_all_repo.get_all(
            filters=TaskFilters(due_date_from=date(2026, 6, 1))
        ).elements
    )

    assert len(result) == 1
    assert result[0].due_date == date(2026, 12, 31)


def test_get_all_filter_by_due_date_to(
    create_repo: CreateTaskSqlalchemyRepository,
    get_all_repo: GetAllTasksSqlalchemyRepository,
) -> None:
    create_repo.create(TaskData(title="T1", description="D", due_date=date(2026, 1, 1)))
    create_repo.create(
        TaskData(title="T2", description="D", due_date=date(2026, 12, 31))
    )

    result = list(
        get_all_repo.get_all(filters=TaskFilters(due_date_to=date(2026, 6, 1))).elements
    )

    assert len(result) == 1
    assert result[0].due_date == date(2026, 1, 1)


def test_get_all_filter_by_title_case_insensitive(
    create_repo: CreateTaskSqlalchemyRepository,
    get_all_repo: GetAllTasksSqlalchemyRepository,
) -> None:
    create_repo.create(
        TaskData(title="Buy Milk", description="D", due_date=date(2026, 5, 1))
    )
    create_repo.create(
        TaskData(title="Walk the dog", description="D", due_date=date(2026, 5, 1))
    )

    result = list(get_all_repo.get_all(filters=TaskFilters(title="BUY")).elements)

    assert len(result) == 1
    assert result[0].title == "Buy Milk"


def test_get_all_combined_filters(
    create_repo: CreateTaskSqlalchemyRepository,
    get_all_repo: GetAllTasksSqlalchemyRepository,
    update_repo: UpdateTaskSqlalchemyRepository,
) -> None:
    create_repo.create(
        TaskData(title="Buy milk", description="D", due_date=date(2026, 5, 1))
    )
    _make_complete(
        create_repo,
        update_repo,
        TaskData(title="Buy eggs", description="D", due_date=date(2026, 5, 1)),
    )

    result = list(
        get_all_repo.get_all(
            filters=TaskFilters(status=TaskStatus.INCOMPLETE, title="buy")
        ).elements
    )

    assert len(result) == 1
    assert result[0].title == "Buy milk"


def test_get_all_filters_applied_before_pagination(
    create_repo: CreateTaskSqlalchemyRepository,
    get_all_repo: GetAllTasksSqlalchemyRepository,
    update_repo: UpdateTaskSqlalchemyRepository,
) -> None:
    create_repo.create(TaskData(title="T1", description="D", due_date=date(2026, 5, 1)))
    create_repo.create(TaskData(title="T2", description="D", due_date=date(2026, 5, 1)))
    _make_complete(
        create_repo,
        update_repo,
        TaskData(title="T3", description="D", due_date=date(2026, 5, 1)),
    )

    result = get_all_repo.get_all(
        filters=TaskFilters(status=TaskStatus.INCOMPLETE), page_size=1
    )

    assert len(list(result.elements)) == 1
    assert result.has_next is True


def test_get_all_empty_filters_returns_all(
    create_repo: CreateTaskSqlalchemyRepository,
    get_all_repo: GetAllTasksSqlalchemyRepository,
) -> None:
    create_repo.create(TASK_DATA)
    create_repo.create(TASK_DATA_2)

    result = list(get_all_repo.get_all(filters=TaskFilters()).elements)

    assert len(result) == 2


def test_get_all_sort_by_title_asc(
    create_repo: CreateTaskSqlalchemyRepository,
    get_all_repo: GetAllTasksSqlalchemyRepository,
) -> None:
    for title in ["Cherry", "Apple", "Banana"]:
        create_repo.create(
            TaskData(title=title, description="D", due_date=date(2026, 5, 1))
        )

    result = list(
        get_all_repo.get_all(
            sort=TaskSort(field=SortField.TITLE, direction=SortDirection.ASC)
        ).elements
    )

    assert [t.title for t in result] == ["Apple", "Banana", "Cherry"]


def test_get_all_sort_by_title_desc(
    create_repo: CreateTaskSqlalchemyRepository,
    get_all_repo: GetAllTasksSqlalchemyRepository,
) -> None:
    for title in ["Apple", "Cherry", "Banana"]:
        create_repo.create(
            TaskData(title=title, description="D", due_date=date(2026, 5, 1))
        )

    result = list(
        get_all_repo.get_all(
            sort=TaskSort(field=SortField.TITLE, direction=SortDirection.DESC)
        ).elements
    )

    assert [t.title for t in result] == ["Cherry", "Banana", "Apple"]


def test_get_all_sort_by_due_date_asc(
    create_repo: CreateTaskSqlalchemyRepository,
    get_all_repo: GetAllTasksSqlalchemyRepository,
) -> None:
    create_repo.create(
        TaskData(title="T1", description="D", due_date=date(2026, 12, 31))
    )
    create_repo.create(TaskData(title="T2", description="D", due_date=date(2026, 1, 1)))

    result = list(
        get_all_repo.get_all(
            sort=TaskSort(field=SortField.DUE_DATE, direction=SortDirection.ASC)
        ).elements
    )

    assert result[0].due_date == date(2026, 1, 1)
    assert result[1].due_date == date(2026, 12, 31)


def test_get_all_sort_by_due_date_desc(
    create_repo: CreateTaskSqlalchemyRepository,
    get_all_repo: GetAllTasksSqlalchemyRepository,
) -> None:
    create_repo.create(TaskData(title="T1", description="D", due_date=date(2026, 1, 1)))
    create_repo.create(
        TaskData(title="T2", description="D", due_date=date(2026, 12, 31))
    )

    result = list(
        get_all_repo.get_all(
            sort=TaskSort(field=SortField.DUE_DATE, direction=SortDirection.DESC)
        ).elements
    )

    assert result[0].due_date == date(2026, 12, 31)
    assert result[1].due_date == date(2026, 1, 1)


def test_get_all_sort_by_status_asc(
    create_repo: CreateTaskSqlalchemyRepository,
    get_all_repo: GetAllTasksSqlalchemyRepository,
    update_repo: UpdateTaskSqlalchemyRepository,
) -> None:
    _make_complete(create_repo, update_repo, TASK_DATA)
    create_repo.create(TASK_DATA_2)

    result = list(
        get_all_repo.get_all(
            sort=TaskSort(field=SortField.STATUS, direction=SortDirection.ASC)
        ).elements
    )

    assert result[0].status == TaskStatus.COMPLETE
    assert result[1].status == TaskStatus.INCOMPLETE


def test_get_all_cursor_works_after_sort_by_title(
    create_repo: CreateTaskSqlalchemyRepository,
    get_all_repo: GetAllTasksSqlalchemyRepository,
) -> None:
    for title in ["Cherry", "Apple", "Banana"]:
        create_repo.create(
            TaskData(title=title, description="D", due_date=date(2026, 5, 1))
        )
    sort = TaskSort(field=SortField.TITLE, direction=SortDirection.ASC)

    page1 = get_all_repo.get_all(sort=sort, page_size=2)
    assert [t.title for t in list(page1.elements)] == ["Apple", "Banana"]

    page2 = list(
        get_all_repo.get_all(
            sort=sort,
            cursor=decode_task_cursor(page1.next_cursor if page1.next_cursor else ""),
            page_size=2,
        ).elements
    )
    assert [t.title for t in page2] == ["Cherry"]


def test_get_all_filter_sort_cursor_pagination_combined(
    create_repo: CreateTaskSqlalchemyRepository,
    get_all_repo: GetAllTasksSqlalchemyRepository,
    update_repo: UpdateTaskSqlalchemyRepository,
) -> None:
    for title in ["Cherry", "Banana", "Date"]:
        create_repo.create(
            TaskData(title=title, description="D", due_date=date(2026, 5, 1))
        )
    _make_complete(
        create_repo,
        update_repo,
        TaskData(title="Apple", description="D", due_date=date(2026, 5, 1)),
    )

    filters = TaskFilters(status=TaskStatus.INCOMPLETE)
    sort = TaskSort(field=SortField.TITLE, direction=SortDirection.ASC)

    page1 = get_all_repo.get_all(filters=filters, sort=sort, page_size=2)
    assert [t.title for t in page1.elements] == ["Banana", "Cherry"]
    assert page1.has_next is True

    page2 = get_all_repo.get_all(
        filters=filters,
        sort=sort,
        cursor=decode_task_cursor(page1.next_cursor if page1.next_cursor else ""),
        page_size=2,
    )
    assert [t.title for t in page2.elements] == ["Date"]
    assert page2.has_next is False


def test_get_task_returns_task_by_id(
    create_repo: CreateTaskSqlalchemyRepository,
    get_repo: GetTaskSqlalchemyRepository,
) -> None:
    created = create_repo.create(TASK_DATA)

    result = get_repo.get_task(created.id)

    assert result.id == created.id
    assert result.title == created.title


def test_get_task_returns_correct_task_among_multiple(
    create_repo: CreateTaskSqlalchemyRepository,
    get_repo: GetTaskSqlalchemyRepository,
) -> None:
    create_repo.create(TASK_DATA)
    created_2 = create_repo.create(TASK_DATA_2)

    result = get_repo.get_task(created_2.id)

    assert result.id == created_2.id
    assert result.title == created_2.title


def test_get_task_raises_not_found_error(
    get_repo: GetTaskSqlalchemyRepository,
) -> None:
    with pytest.raises(NotFoundError):
        get_repo.get_task(999)


def test_update_persists_changes(
    create_repo: CreateTaskSqlalchemyRepository,
    get_repo: GetTaskSqlalchemyRepository,
    update_repo: UpdateTaskSqlalchemyRepository,
) -> None:
    created = create_repo.create(TASK_DATA)
    update_data = TaskUpdateData(
        title="Buy eggs",
        description="At the market",
        due_date=date(2026, 6, 1),
        status=TaskStatus.COMPLETE,
    )

    update_repo.update(created.id, update_data)

    updated = get_repo.get_task(created.id)
    assert updated.title == "Buy eggs"
    assert updated.description == "At the market"
    assert updated.due_date == date(2026, 6, 1)
    assert updated.status == TaskStatus.COMPLETE


def test_update_raises_not_found_error(
    update_repo: UpdateTaskSqlalchemyRepository,
) -> None:
    update_data = TaskUpdateData(
        title="X",
        description="X",
        due_date=date(2026, 1, 1),
        status=TaskStatus.COMPLETE,
    )

    with pytest.raises(NotFoundError):
        update_repo.update(999, update_data)


def test_delete_removes_task(
    create_repo: CreateTaskSqlalchemyRepository,
    get_all_repo: GetAllTasksSqlalchemyRepository,
    delete_repo: DeleteTaskSqlalchemyRepository,
) -> None:
    created = create_repo.create(TASK_DATA)

    delete_repo.delete_task(created.id)

    assert list(get_all_repo.get_all().elements) == []


def test_delete_raises_not_found_error(
    delete_repo: DeleteTaskSqlalchemyRepository,
) -> None:
    with pytest.raises(NotFoundError):
        delete_repo.delete_task(999)
