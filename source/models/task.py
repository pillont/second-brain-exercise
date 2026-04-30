from dataclasses import dataclass
from datetime import date
from enum import StrEnum


class TaskStatus(StrEnum):
    INCOMPLETE = "Incomplete"
    COMPLETE = "Complete"


@dataclass
class TaskData:
    title: str
    description: str
    due_date: date


@dataclass
class TaskUpdateData(TaskData):
    status: TaskStatus


@dataclass
class Task:
    id: int
    title: str
    description: str
    due_date: date
    status: TaskStatus
