from dataclasses import dataclass
from datetime import date
from source.models.task import TaskStatus
from source.controllers.entities.link import Links


@dataclass
class TaskDataEntity:
    title: str
    description: str
    due_date: date


@dataclass
class TaskEntity:
    id: int
    title: str
    description: str
    due_date: date
    status: TaskStatus
    links: Links
