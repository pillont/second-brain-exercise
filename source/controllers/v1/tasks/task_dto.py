from datetime import date
from typing import TypedDict

from source.controllers.v1.utils.link import LinkDTO, LinksListDTO
from source.models.task import TaskStatus


class TaskLinksDTO(LinksListDTO):
    tasks: LinkDTO
    update: LinkDTO
    delete: LinkDTO


class TaskDataDTO(TypedDict):
    title: str
    description: str
    due_date: date


class TaskUpdateDataDTO(TaskDataDTO):
    status: TaskStatus


class TaskDTO(TypedDict):
    id: int
    title: str
    description: str
    due_date: date
    status: TaskStatus
    links: TaskLinksDTO
