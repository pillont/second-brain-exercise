from datetime import date
from typing import Optional

from source.controllers.entities.list_argument_entity import ListArgumentEntity
from source.models.task import TaskStatus


class TasksListArgumentEntity(ListArgumentEntity):
    status: Optional[TaskStatus]
    due_date_from: Optional[date]
    due_date_to: Optional[date]
    title: Optional[str]
    description: Optional[str]
