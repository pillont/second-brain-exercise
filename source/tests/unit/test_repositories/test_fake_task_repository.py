from datetime import date
from source.models.task import Task, TaskData, TaskStatus, TaskUpdateData
from source.repositories.fake.tasks_fake_repository import TasksFakeRepository


def test_create_returns_task() -> None:
    repo = TasksFakeRepository()
    task_data = TaskData(
        title="Buy milk", description="At the store", due_date=date(2026, 5, 1)
    )

    result = repo.create(task_data)

    assert isinstance(result, Task)


def test_create_assigns_id_starting_at_one() -> None:
    repo = TasksFakeRepository()
    task_data = TaskData(
        title="Buy milk", description="At the store", due_date=date(2026, 5, 1)
    )

    result = repo.create(task_data)

    assert result.id == 1


def test_create_increments_id() -> None:
    repo = TasksFakeRepository()
    task_data = TaskData(
        title="Buy milk", description="At the store", due_date=date(2026, 5, 1)
    )

    first = repo.create(task_data)
    second = repo.create(task_data)

    assert first.id == 1
    assert second.id == 2


def test_create_sets_status_incomplete() -> None:
    repo = TasksFakeRepository()
    task_data = TaskData(
        title="Buy milk", description="At the store", due_date=date(2026, 5, 1)
    )

    result = repo.create(task_data)

    assert result.status == TaskStatus.INCOMPLETE


def test_create_stores_task_data() -> None:
    repo = TasksFakeRepository()
    task_data = TaskData(
        title="Buy milk", description="At the store", due_date=date(2026, 5, 1)
    )

    result = repo.create(task_data)

    assert result.title == "Buy milk"
    assert result.description == "At the store"
    assert result.due_date == date(2026, 5, 1)


def test_get_all_returns_empty_initially() -> None:
    repo = TasksFakeRepository()

    result = list(repo.get_all().elements)

    assert result == []


def test_get_all_returns_created_task() -> None:
    repo = TasksFakeRepository()
    task_data = TaskData(
        title="Buy milk", description="At the store", due_date=date(2026, 5, 1)
    )
    created = repo.create(task_data)

    result = list(repo.get_all().elements)

    assert len(result) == 1
    assert result[0] is created


def test_get_all_returns_multiple_tasks_in_order() -> None:
    repo = TasksFakeRepository()
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
    repo = TasksFakeRepository()
    task_data = TaskData(
        title="Buy milk", description="At the store", due_date=date(2026, 5, 1)
    )
    repo.create(task_data)

    result = repo.get_all().elements

    assert hasattr(result, "__iter__")


def test_get_all_returns_all_values_by_default() -> None:
    repo = TasksFakeRepository()

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
    repo = TasksFakeRepository()

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
    repo = TasksFakeRepository()

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
    repo = TasksFakeRepository()

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
    repo = TasksFakeRepository()

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
    repo = TasksFakeRepository()

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
    repo = TasksFakeRepository()

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
    repo = TasksFakeRepository()
    task_data = TaskData(
        title="Buy milk", description="At the store", due_date=date(2026, 5, 1)
    )
    repo.create(task_data)

    list(repo.get_all().elements)
    result = list(repo.get_all().elements)

    assert len(result) == 1


def test_get_task_returns_task_by_id() -> None:
    repo = TasksFakeRepository()
    task_data = TaskData(
        title="Buy milk", description="At the store", due_date=date(2026, 5, 1)
    )
    created = repo.create(task_data)

    result = repo.get_task(created.id)

    assert result is created


def test_get_task_returns_correct_task_among_multiple() -> None:
    repo = TasksFakeRepository()
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

    repo = TasksFakeRepository()

    try:
        repo.get_task(99)
        assert False, "Expected NotFoundError to be raised"
    except NotFoundError:
        pass


def test_get_task_raises_not_found_error_after_all_tasks_consumed() -> None:
    from source.models.not_found_error import NotFoundError

    repo = TasksFakeRepository()
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
    repo = TasksFakeRepository()
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


def test_get_all_with_status_filter_returns_matching_tasks() -> None:
    repo = TasksFakeRepository()
    created = repo.create(
        TaskData(
            title="Buy milk", description="At the store", due_date=date(2026, 5, 1)
        )
    )
    repo.update(
        created.id,
        TaskUpdateData(
            title=created.title,
            description=created.description,
            due_date=created.due_date,
            status=TaskStatus.COMPLETE,
        ),
    )
    repo.create(
        TaskData(
            title="Buy eggs", description="At the market", due_date=date(2026, 5, 2)
        )
    )

    from source.models.task_filters import TaskFilters

    result = list(
        repo.get_all(filters=TaskFilters(status=TaskStatus.COMPLETE)).elements
    )

    assert len(result) == 1
    assert result[0].status == TaskStatus.COMPLETE


def test_get_all_with_status_filter_excludes_non_matching_tasks() -> None:
    repo = TasksFakeRepository()
    created = repo.create(
        TaskData(
            title="Buy milk", description="At the store", due_date=date(2026, 5, 1)
        )
    )
    repo.update(
        created.id,
        TaskUpdateData(
            title=created.title,
            description=created.description,
            due_date=created.due_date,
            status=TaskStatus.COMPLETE,
        ),
    )
    repo.create(
        TaskData(
            title="Buy eggs", description="At the market", due_date=date(2026, 5, 2)
        )
    )

    from source.models.task_filters import TaskFilters

    result = list(
        repo.get_all(filters=TaskFilters(status=TaskStatus.INCOMPLETE)).elements
    )

    assert len(result) == 1
    assert result[0].status == TaskStatus.INCOMPLETE


def test_get_all_with_due_date_from_filter() -> None:
    repo = TasksFakeRepository()
    repo.create(TaskData(title="Task 1", description="Desc", due_date=date(2026, 1, 1)))
    repo.create(
        TaskData(title="Task 2", description="Desc", due_date=date(2026, 12, 31))
    )

    from source.models.task_filters import TaskFilters

    result = list(
        repo.get_all(filters=TaskFilters(due_date_from=date(2026, 6, 1))).elements
    )

    assert len(result) == 1
    assert result[0].due_date == date(2026, 12, 31)


def test_get_all_with_due_date_to_filter() -> None:
    repo = TasksFakeRepository()
    repo.create(TaskData(title="Task 1", description="Desc", due_date=date(2026, 1, 1)))
    repo.create(
        TaskData(title="Task 2", description="Desc", due_date=date(2026, 12, 31))
    )

    from source.models.task_filters import TaskFilters

    result = list(
        repo.get_all(filters=TaskFilters(due_date_to=date(2026, 6, 1))).elements
    )

    assert len(result) == 1
    assert result[0].due_date == date(2026, 1, 1)


def test_get_all_with_title_filter_case_insensitive() -> None:
    repo = TasksFakeRepository()
    repo.create(
        TaskData(title="Buy Milk", description="Desc", due_date=date(2026, 5, 1))
    )
    repo.create(
        TaskData(title="Walk the dog", description="Desc", due_date=date(2026, 5, 1))
    )

    from source.models.task_filters import TaskFilters

    result = list(repo.get_all(filters=TaskFilters(title="buy")).elements)

    assert len(result) == 1
    assert result[0].title == "Buy Milk"


def test_get_all_with_combined_filters() -> None:
    repo = TasksFakeRepository()
    repo.create(
        TaskData(title="Buy milk", description="Desc", due_date=date(2026, 5, 1))
    )
    created = repo.create(
        TaskData(title="Buy eggs", description="Desc", due_date=date(2026, 5, 1))
    )
    repo.update(
        created.id,
        TaskUpdateData(
            title=created.title,
            description=created.description,
            due_date=created.due_date,
            status=TaskStatus.COMPLETE,
        ),
    )

    from source.models.task_filters import TaskFilters

    result = list(
        repo.get_all(
            filters=TaskFilters(status=TaskStatus.INCOMPLETE, title="buy")
        ).elements
    )

    assert len(result) == 1
    assert result[0].title == "Buy milk"


def test_get_all_filters_applied_before_pagination() -> None:
    repo = TasksFakeRepository()
    repo.create(TaskData(title="Task 1", description="Desc", due_date=date(2026, 5, 1)))
    repo.create(TaskData(title="Task 2", description="Desc", due_date=date(2026, 5, 1)))
    created = repo.create(
        TaskData(title="Task 3", description="Desc", due_date=date(2026, 5, 1))
    )
    repo.update(
        created.id,
        TaskUpdateData(
            title=created.title,
            description=created.description,
            due_date=created.due_date,
            status=TaskStatus.COMPLETE,
        ),
    )

    from source.models.task_filters import TaskFilters

    result = repo.get_all(
        filters=TaskFilters(status=TaskStatus.INCOMPLETE), page_size=1
    )

    assert len(list(result.elements)) == 1
    assert result.has_next is True


def test_get_all_with_empty_filters_returns_all_tasks() -> None:
    repo = TasksFakeRepository()
    repo.create(TaskData(title="Task 1", description="Desc", due_date=date(2026, 5, 1)))
    repo.create(TaskData(title="Task 2", description="Desc", due_date=date(2026, 5, 1)))

    from source.models.task_filters import TaskFilters

    result = list(repo.get_all(filters=TaskFilters()).elements)

    assert len(result) == 2


def test_update_task_raises_not_found_error_for_unknown_id() -> None:
    from source.models.not_found_error import NotFoundError

    repo = TasksFakeRepository()
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


def test_get_all_sort_by_title_asc() -> None:
    from source.models.task_sort import SortField, SortDirection, TaskSort

    repo = TasksFakeRepository()
    repo.create(TaskData(title="Cherry", description="Desc", due_date=date(2026, 5, 1)))
    repo.create(TaskData(title="Apple", description="Desc", due_date=date(2026, 5, 1)))
    repo.create(TaskData(title="Banana", description="Desc", due_date=date(2026, 5, 1)))

    result = list(
        repo.get_all(
            sort=TaskSort(field=SortField.TITLE, direction=SortDirection.ASC)
        ).elements
    )

    assert [t.title for t in result] == ["Apple", "Banana", "Cherry"]


def test_get_all_sort_by_title_desc() -> None:
    from source.models.task_sort import SortField, SortDirection, TaskSort

    repo = TasksFakeRepository()
    repo.create(TaskData(title="Apple", description="Desc", due_date=date(2026, 5, 1)))
    repo.create(TaskData(title="Cherry", description="Desc", due_date=date(2026, 5, 1)))
    repo.create(TaskData(title="Banana", description="Desc", due_date=date(2026, 5, 1)))

    result = list(
        repo.get_all(
            sort=TaskSort(field=SortField.TITLE, direction=SortDirection.DESC)
        ).elements
    )

    assert [t.title for t in result] == ["Cherry", "Banana", "Apple"]


def test_get_all_sort_by_due_date_asc() -> None:
    from source.models.task_sort import SortField, SortDirection, TaskSort

    repo = TasksFakeRepository()
    repo.create(
        TaskData(title="Task 1", description="Desc", due_date=date(2026, 12, 31))
    )
    repo.create(TaskData(title="Task 2", description="Desc", due_date=date(2026, 1, 1)))
    repo.create(TaskData(title="Task 3", description="Desc", due_date=date(2026, 6, 1)))

    result = list(
        repo.get_all(
            sort=TaskSort(field=SortField.DUE_DATE, direction=SortDirection.ASC)
        ).elements
    )

    assert [t.due_date for t in result] == [
        date(2026, 1, 1),
        date(2026, 6, 1),
        date(2026, 12, 31),
    ]


def test_get_all_sort_by_due_date_desc() -> None:
    from source.models.task_sort import SortField, SortDirection, TaskSort

    repo = TasksFakeRepository()
    repo.create(TaskData(title="Task 1", description="Desc", due_date=date(2026, 1, 1)))
    repo.create(
        TaskData(title="Task 2", description="Desc", due_date=date(2026, 12, 31))
    )

    result = list(
        repo.get_all(
            sort=TaskSort(field=SortField.DUE_DATE, direction=SortDirection.DESC)
        ).elements
    )

    assert result[0].due_date == date(2026, 12, 31)
    assert result[1].due_date == date(2026, 1, 1)


def test_get_all_sort_by_status_asc() -> None:
    from source.models.task_sort import SortField, SortDirection, TaskSort

    repo = TasksFakeRepository()
    created = repo.create(
        TaskData(title="Task 1", description="Desc", due_date=date(2026, 5, 1))
    )
    repo.update(
        created.id,
        TaskUpdateData(
            title=created.title,
            description=created.description,
            due_date=created.due_date,
            status=TaskStatus.COMPLETE,
        ),
    )
    repo.create(TaskData(title="Task 2", description="Desc", due_date=date(2026, 5, 1)))

    result = list(
        repo.get_all(
            sort=TaskSort(field=SortField.STATUS, direction=SortDirection.ASC)
        ).elements
    )

    assert result[0].status == TaskStatus.COMPLETE
    assert result[1].status == TaskStatus.INCOMPLETE


def test_get_all_cursor_works_correctly_after_sort_by_title() -> None:
    from source.models.task_sort import SortField, SortDirection, TaskSort

    repo = TasksFakeRepository()
    repo.create(TaskData(title="Cherry", description="Desc", due_date=date(2026, 5, 1)))
    repo.create(TaskData(title="Apple", description="Desc", due_date=date(2026, 5, 1)))
    repo.create(TaskData(title="Banana", description="Desc", due_date=date(2026, 5, 1)))

    sort = TaskSort(field=SortField.TITLE, direction=SortDirection.ASC)
    page1 = list(repo.get_all(sort=sort, page_size=2).elements)
    assert [t.title for t in page1] == ["Apple", "Banana"]
    assert repo.get_all(sort=sort, page_size=2).has_next is True

    cursor_id = page1[-1].id
    page2 = list(repo.get_all(sort=sort, cursor=cursor_id, page_size=2).elements)
    assert [t.title for t in page2] == ["Cherry"]
    assert repo.get_all(sort=sort, cursor=cursor_id, page_size=2).has_next is False


def test_get_all_cursor_not_found_returns_full_sorted_list() -> None:
    from source.models.task_sort import SortField, SortDirection, TaskSort

    repo = TasksFakeRepository()
    repo.create(TaskData(title="Cherry", description="Desc", due_date=date(2026, 5, 1)))
    repo.create(TaskData(title="Apple", description="Desc", due_date=date(2026, 5, 1)))

    sort = TaskSort(field=SortField.TITLE, direction=SortDirection.ASC)
    result = list(repo.get_all(sort=sort, cursor=999).elements)

    assert [t.title for t in result] == ["Apple", "Cherry"]


def test_get_all_filter_and_sort_combined() -> None:
    from source.models.task_filters import TaskFilters
    from source.models.task_sort import SortField, SortDirection, TaskSort

    repo = TasksFakeRepository()
    repo.create(TaskData(title="Cherry", description="Desc", due_date=date(2026, 5, 1)))
    created = repo.create(
        TaskData(title="Apple", description="Desc", due_date=date(2026, 5, 1))
    )
    repo.update(
        created.id,
        TaskUpdateData(
            title=created.title,
            description=created.description,
            due_date=created.due_date,
            status=TaskStatus.COMPLETE,
        ),
    )
    repo.create(TaskData(title="Banana", description="Desc", due_date=date(2026, 5, 1)))

    result = list(
        repo.get_all(
            filters=TaskFilters(status=TaskStatus.INCOMPLETE),
            sort=TaskSort(field=SortField.TITLE, direction=SortDirection.ASC),
        ).elements
    )

    assert [t.title for t in result] == ["Banana", "Cherry"]


def test_get_all_filter_sort_cursor_pagination_combined() -> None:
    from source.models.task_filters import TaskFilters
    from source.models.task_sort import SortField, SortDirection, TaskSort

    repo = TasksFakeRepository()
    repo.create(TaskData(title="Cherry", description="Desc", due_date=date(2026, 5, 1)))
    created = repo.create(
        TaskData(title="Apple", description="Desc", due_date=date(2026, 5, 1))
    )
    repo.update(
        created.id,
        TaskUpdateData(
            title=created.title,
            description=created.description,
            due_date=created.due_date,
            status=TaskStatus.COMPLETE,
        ),
    )
    repo.create(TaskData(title="Banana", description="Desc", due_date=date(2026, 5, 1)))
    repo.create(TaskData(title="Date", description="Desc", due_date=date(2026, 5, 1)))

    filters = TaskFilters(status=TaskStatus.INCOMPLETE)
    sort = TaskSort(field=SortField.TITLE, direction=SortDirection.ASC)

    page1 = repo.get_all(filters=filters, sort=sort, page_size=2)
    assert [t.title for t in page1.elements] == ["Banana", "Cherry"]
    assert page1.has_next is True

    cursor_id = list(repo.get_all(filters=filters, sort=sort, page_size=2).elements)[
        -1
    ].id
    page2 = repo.get_all(filters=filters, sort=sort, cursor=cursor_id, page_size=2)
    assert [t.title for t in page2.elements] == ["Date"]
    assert page2.has_next is False


def test_get_all_none_sort_preserves_insertion_order() -> None:
    repo = TasksFakeRepository()
    repo.create(TaskData(title="Cherry", description="Desc", due_date=date(2026, 5, 1)))
    repo.create(TaskData(title="Apple", description="Desc", due_date=date(2026, 5, 1)))
    repo.create(TaskData(title="Banana", description="Desc", due_date=date(2026, 5, 1)))

    result = list(repo.get_all(sort=None).elements)

    assert [t.title for t in result] == ["Cherry", "Apple", "Banana"]
