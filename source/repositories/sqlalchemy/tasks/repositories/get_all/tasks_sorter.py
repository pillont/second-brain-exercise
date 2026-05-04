from typing import Any, Optional

from sqlalchemy import Select, func

from source.models.task_sort import SortDirection, SortField, TaskSort
from source.repositories.sqlalchemy.tasks.task_orm_model import TaskOrmModel


def _get_sort_column(sort: TaskSort) -> Any:
    match sort.field:
        case SortField.TITLE:
            return func.lower(TaskOrmModel.title)
        case SortField.DUE_DATE:
            return TaskOrmModel.due_date
        case SortField.STATUS:
            return TaskOrmModel.status
        case _:
            return TaskOrmModel.id


def _get_sort_expression(sort) -> Any:
    sort_column = _get_sort_column(sort)
    reverse = sort.direction == SortDirection.DESC
    sort_fn = sort_column.desc() if reverse else sort_column.asc()

    return sort_fn


def apply_sort(select_statement: Select, sort: Optional[TaskSort]) -> Select:
    if not sort:
        return select_statement

    sort_fn = _get_sort_expression(sort)
    return select_statement.order_by(sort_fn)
