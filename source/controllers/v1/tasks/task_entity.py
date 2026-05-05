from datetime import date
from typing import TypedDict

from source.controllers.v1.utils.link import LinkEntity, LinksEntity
from source.models.task import TaskStatus


class TaskLinks(LinksEntity):
    tasks: LinkEntity
    update: LinkEntity
    delete: LinkEntity


class TaskDataEntity(TypedDict):
    title: str
    description: str
    due_date: date


class TaskUpdateDataEntity(TaskDataEntity):
    status: TaskStatus


class TaskEntity(TypedDict):
    id: int
    title: str
    description: str
    due_date: date
    status: TaskStatus
    links: TaskLinks
