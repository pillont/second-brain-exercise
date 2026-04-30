from dataclasses import dataclass
from datetime import date
from source.models.task import TaskStatus
from source.controllers.entities.link import Link, Links

@dataclass
class TaskLinks(Links):
    tasks: Link


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
    links: TaskLinks
