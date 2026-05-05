from typing import Final, List, Optional

from sqlalchemy import select
from sqlalchemy.engine import Engine
from sqlalchemy.sql import Select

from source.models.filtered_list import FilteredList, map_to_filtered_list
from source.models.task import Task
from source.models.task_cursor import TaskCursor, encode_task_cursor
from source.models.task_filters import TaskFilters
from source.models.task_sort import TaskSort
from source.repositories.get_all_tasks_repository import GetAllTasksRepository
from source.repositories.sqlalchemy.session_utils import (OrmSession,
                                                          initialize_schema)
from source.repositories.sqlalchemy.tasks.repositories.create.task_sqlalchemy_mapper import \
    to_task
from source.repositories.sqlalchemy.tasks.repositories.get_all.task_cursor import \
    apply_cursor
from source.repositories.sqlalchemy.tasks.repositories.get_all.tasks_sorter import \
    apply_sort
from source.repositories.sqlalchemy.tasks.repositories.get_all.tasks_statement_filter import \
    apply_tasks_filters
from source.repositories.sqlalchemy.tasks.task_orm_model import TaskOrmModel


def _build_query_without_cursor(
    filters: Optional[TaskFilters],
    sort: Optional[TaskSort],
) -> Select:
    select_statement = select(TaskOrmModel)
    filtered_tasks = apply_tasks_filters(select_statement, filters)
    return apply_sort(filtered_tasks, sort)


def _compute_next_cursor(
    tasks: List[Task], page_size: int, sort: Optional[TaskSort]
) -> Optional[str]:
    if len(tasks) < page_size:
        return None
    last_task = tasks[page_size - 1]
    return encode_task_cursor(last_task, sort or TaskSort())


class GetAllTasksSqlalchemyRepository(GetAllTasksRepository):
    def __init__(self, engine: Engine) -> None:
        self._orm_session: Final = OrmSession(initialize_schema(engine), TaskOrmModel)

    def get_all(
        self,
        filters: Optional[TaskFilters] = None,
        sort: Optional[TaskSort] = None,
        cursor: Optional[TaskCursor] = None,
        page_size: Optional[int] = None,
    ) -> FilteredList[Task]:
        query = _build_query_without_cursor(filters, sort)
        if cursor:
            query = apply_cursor(query, sort, cursor)
        return self._build_filtered_list(query, sort, page_size)

    def _build_filtered_list(
        self,
        query: Select,
        sort: Optional[TaskSort],
        page_size: Optional[int],
    ) -> FilteredList[Task]:
        tasks = [to_task(t) for t in self._orm_session.select(query)]
        filtered = map_to_filtered_list(tasks, page_size)
        next_cursor = (
            _compute_next_cursor(tasks, page_size, sort)
            if page_size and filtered.has_next
            else None
        )
        return FilteredList(filtered.elements, filtered.has_next, next_cursor)
