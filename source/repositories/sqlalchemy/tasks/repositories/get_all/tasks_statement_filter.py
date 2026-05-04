
from datetime import date
from typing import Optional

from sqlalchemy import Select, func

from source.models.task import TaskStatus
from source.models.task_filters import TaskFilters
from source.repositories.sqlalchemy.tasks.task_orm_model import TaskOrmModel


def _filter_by_status(select_statement: Select, status: TaskStatus) -> Select:
    return select_statement.where(TaskOrmModel.status == str(status))


def _filter_by_due_date_from(select_statement: Select, due_date_from: date) -> Select:
    return select_statement.where(TaskOrmModel.due_date >= due_date_from)


def _filter_by_due_date_to(select_statement: Select, due_date_to: date) -> Select:
    return select_statement.where(TaskOrmModel.due_date <= due_date_to)


def _filter_by_title(select_statement: Select, title: str) -> Select:
    return select_statement.where(
        func.lower(TaskOrmModel.title).contains(title.lower())
    )

def apply_tasks_filters(
    select_statement: Select, filters: Optional[TaskFilters]
) -> Select:
    if not filters:
        return select_statement
    
    if filters.status:
        select_statement = _filter_by_status(select_statement, filters.status)
    
    if filters.due_date_from:
        select_statement = _filter_by_due_date_from(
            select_statement, filters.due_date_from
        )
    
    if filters.due_date_to:
        select_statement = _filter_by_due_date_to(
            select_statement, filters.due_date_to
        )
    
    if filters.title:
        select_statement = _filter_by_title(select_statement, filters.title)
        
    return select_statement
