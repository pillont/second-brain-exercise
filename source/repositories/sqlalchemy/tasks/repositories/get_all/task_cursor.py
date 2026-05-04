from typing import Any, Optional

from sqlalchemy import and_, func, or_
from sqlalchemy.sql import Select

from source.models.task_cursor import TaskCursor, convert_cursor_sort_value
from source.models.task_sort import SortDirection, SortField, TaskSort
from source.repositories.sqlalchemy.tasks.task_orm_model import TaskOrmModel


def apply_cursor(
    select_statement: Select, sort: Optional[TaskSort], task_cursor: TaskCursor
) -> Select:
    field = sort.field if sort else SortField.ID
    asc = (sort.direction if sort else SortDirection.ASC) == SortDirection.ASC
    cursor_id = task_cursor.id
    val = convert_cursor_sort_value(task_cursor.sort_value, field)

    if field == SortField.ID:
        return select_statement.where(
            TaskOrmModel.id > cursor_id if asc else TaskOrmModel.id < cursor_id
        )

    col = _get_cursor_col(field)
    return select_statement.where(
        or_(
            col > val if asc else col < val,
            and_(col == val, TaskOrmModel.id > cursor_id),
        )
    )


def _get_cursor_col(field: SortField) -> Any:
    match field:
        case SortField.TITLE:
            return func.lower(TaskOrmModel.title)
        case SortField.DUE_DATE:
            return TaskOrmModel.due_date
        case SortField.STATUS:
            return TaskOrmModel.status
        case _:
            raise NotImplementedError()
