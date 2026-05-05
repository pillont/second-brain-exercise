from datetime import date
from typing import Optional

from source.controllers.v1.entities.list_argument_entity import \
    ListArgumentEntity
from source.models.task import TaskStatus
from source.models.task_sort import SortDirection, SortField


class TasksListArgumentEntity(ListArgumentEntity):
    status: Optional[TaskStatus]
    due_date_from: Optional[date]
    due_date_to: Optional[date]
    title: Optional[str]
    sort_by: Optional[SortField]
    sort_direction: Optional[SortDirection]
