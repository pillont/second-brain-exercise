from typing import Any, Optional

from sqlalchemy import and_, func, or_
from sqlalchemy.sql import Select

from source.models.task import Task
from source.models.task_sort import SortDirection, SortField, TaskSort
from source.repositories.sqlalchemy.session_utils import OrmSession
from source.repositories.sqlalchemy.tasks.task_orm_model import TaskOrmModel


def _get_cursor_val(field: SortField, cursor_row: TaskOrmModel) -> Any:
    match field:
        case SortField.TITLE:
            return cursor_row.title.lower()
        case SortField.DUE_DATE:
            return cursor_row.due_date
        case SortField.STATUS:
            return cursor_row.status
        case _:
            raise NotImplementedError()

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

def apply_cursor(
    select_statement: Select, sort: Optional[TaskSort], cursor_row: TaskOrmModel
) -> Select:
    cursor_id = cursor_row.id
    field = sort.field if sort else SortField.ID
    asc = (sort.direction if sort else SortDirection.ASC) == SortDirection.ASC

    if field == SortField.ID:
        return select_statement.where(
            TaskOrmModel.id > cursor_id if asc else TaskOrmModel.id < cursor_id
        )

    col = _get_cursor_col(field)
    val = _get_cursor_val(field, cursor_row)

    return select_statement.where(
            or_(
                (
                    col > val 
                    if asc 
                    else col < val
                ), 
                and_(
                    col == val, 
                    TaskOrmModel.id > cursor_id)
                )
        )

def get_cursor_row(orm_session: OrmSession[TaskOrmModel], cursor: int) -> TaskOrmModel:
    return orm_session.get_or_raise(cursor)
