import base64
import json
from datetime import date
from typing import Final, TypedDict, Union

from source.models.task import Task, TaskStatus
from source.models.task_sort import SortField, TaskSort


class _TaskCursorPayload(TypedDict):
    v: str
    id: int


class TaskCursor:
    def __init__(self, sort_value: str, id: int) -> None:
        self.sort_value: Final = sort_value
        self.id: Final = id


def encode_task_cursor(task: Task, sort: TaskSort) -> str:
    value = _extract_sort_value(task, sort.field)
    payload: _TaskCursorPayload = {"v": value, "id": task.id}
    return base64.b64encode(json.dumps(payload).encode()).decode()


def decode_task_cursor(cursor_b64: str) -> TaskCursor:
    payload: _TaskCursorPayload = json.loads(base64.b64decode(cursor_b64).decode())
    return TaskCursor(sort_value=payload["v"], id=payload["id"])


def convert_cursor_sort_value(
    sort_value: str, field: SortField
) -> Union[str, int, date, TaskStatus]:
    match field:
        case SortField.ID:
            return int(sort_value)
        case SortField.TITLE:
            return sort_value
        case SortField.DUE_DATE:
            return date.fromisoformat(sort_value)
        case SortField.STATUS:
            return TaskStatus(sort_value)


def _extract_sort_value(task: Task, field: SortField) -> str:
    match field:
        case SortField.TITLE:
            return task.title.lower()
        case SortField.DUE_DATE:
            return task.due_date.isoformat()
        case SortField.STATUS:
            return task.status
        case _:
            return str(task.id)
