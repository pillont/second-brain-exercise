from typing import Any, Final, Iterable, List, Optional

from sqlalchemy import and_, func, or_, select
from sqlalchemy.engine import Engine
from sqlalchemy.sql import Select

from source.models.filtered_list import FilteredList, map_to_filtered_list
from source.models.task import Task
from source.models.task_filters import TaskFilters
from source.models.task_sort import TaskSort
from source.repositories.get_all_tasks_repository import GetAllTasksRepository
from source.repositories.sqlalchemy.tasks.repositories.get_all.task_cursor import (
    apply_cursor,
    get_cursor_row,
)
from source.repositories.sqlalchemy.tasks.repositories.get_all.tasks_sorter import (
    apply_sort,
)
from source.repositories.sqlalchemy.session_utils import OrmSession, initialize_schema
from source.repositories.sqlalchemy.tasks.task_orm_model import TaskOrmModel
from source.repositories.sqlalchemy.tasks.repositories.create.task_sqlalchemy_mapper import (
    to_task,
)
from source.repositories.sqlalchemy.tasks.repositories.get_all.tasks_statement_filter import (
    apply_tasks_filters,
)


def _build_query_without_cursor(
    filters: Optional[TaskFilters],
    sort: Optional[TaskSort],
) -> Select:
    select_statement = select(TaskOrmModel)
    filtered_tasks = apply_tasks_filters(select_statement, filters)
    query = apply_sort(filtered_tasks, sort)
    return query


class GetAllTasksSqlalchemyRepository(GetAllTasksRepository):
    def __init__(self, engine: Engine) -> None:
        self._orm_session: Final = OrmSession(initialize_schema(engine), TaskOrmModel)

    def get_all(
        self,
        filters: Optional[TaskFilters] = None,
        sort: Optional[TaskSort] = None,
        cursor: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> FilteredList[Task]:
        query = self._build_get_all_query(filters, sort, cursor)
        return self._map_to_filtered_tasks_list(query, page_size)

    def _map_to_filtered_tasks_list(
        self, query: Select, page_size: Optional[int]
    ) -> FilteredList[Task]:
        tasks = self._execute_query(query)
        return map_to_filtered_list(tasks, page_size)

    def _execute_query(self, query: Select) -> Iterable[Task]:
        return (to_task(t) for t in self._orm_session.select(query))

    def _build_get_all_query(
        self,
        filters: Optional[TaskFilters],
        sort: Optional[TaskSort],
        cursor: Optional[int],
    ) -> Select:
        query = _build_query_without_cursor(filters, sort)
        if not cursor:
            return query

        return self._apply_cursor_on_query(query, cursor, sort)

    def _apply_cursor_on_query(
        self, query: Select, cursor: int, sort: Optional[TaskSort]
    ) -> Select:
        cursor_row = get_cursor_row(self._orm_session, cursor)
        if not cursor_row:
            raise NotImplementedError()

        query = apply_cursor(query, sort, cursor_row)
        return query
