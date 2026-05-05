from datetime import date

from source.models.task import Task, TaskStatus
from source.models.task_cursor import (TaskCursor, convert_cursor_sort_value,
                                       decode_task_cursor, encode_task_cursor)
from source.models.task_sort import SortDirection, SortField, TaskSort

TASK = Task(
    id=5,
    title="Buy Milk",
    description="At the store",
    due_date=date(2026, 3, 15),
    status=TaskStatus.INCOMPLETE,
)


def test_encode_decode_round_trip_by_id() -> None:
    sort = TaskSort(field=SortField.ID, direction=SortDirection.ASC)
    cursor_b64 = encode_task_cursor(TASK, sort)
    cursor = decode_task_cursor(cursor_b64)

    assert cursor.sort_value == "5"
    assert cursor.id == 5


def test_encode_decode_round_trip_by_title() -> None:
    sort = TaskSort(field=SortField.TITLE, direction=SortDirection.ASC)
    cursor_b64 = encode_task_cursor(TASK, sort)
    cursor = decode_task_cursor(cursor_b64)

    assert cursor.sort_value == "buy milk"
    assert cursor.id == 5


def test_encode_decode_round_trip_by_due_date() -> None:
    sort = TaskSort(field=SortField.DUE_DATE, direction=SortDirection.ASC)
    cursor_b64 = encode_task_cursor(TASK, sort)
    cursor = decode_task_cursor(cursor_b64)

    assert cursor.sort_value == "2026-03-15"
    assert cursor.id == 5


def test_encode_decode_round_trip_by_status() -> None:
    sort = TaskSort(field=SortField.STATUS, direction=SortDirection.ASC)
    cursor_b64 = encode_task_cursor(TASK, sort)
    cursor = decode_task_cursor(cursor_b64)

    assert cursor.sort_value == TaskStatus.INCOMPLETE
    assert cursor.id == 5


def test_convert_cursor_sort_value_id() -> None:
    result = convert_cursor_sort_value("5", SortField.ID)
    assert result == 5


def test_convert_cursor_sort_value_title() -> None:
    result = convert_cursor_sort_value("buy milk", SortField.TITLE)
    assert result == "buy milk"


def test_convert_cursor_sort_value_due_date() -> None:
    result = convert_cursor_sort_value("2026-03-15", SortField.DUE_DATE)
    assert result == date(2026, 3, 15)


def test_convert_cursor_sort_value_status() -> None:
    result = convert_cursor_sort_value(TaskStatus.INCOMPLETE, SortField.STATUS)
    assert result == TaskStatus.INCOMPLETE


def test_task_cursor_holds_values() -> None:
    cursor = TaskCursor(sort_value="banana", id=3)
    assert cursor.sort_value == "banana"
    assert cursor.id == 3
