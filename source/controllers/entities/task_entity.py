from dataclasses import dataclass
from datetime import date
from typing import TypedDict
from source.models.task import TaskStatus
from source.controllers.entities.link import LinkEntity, LinksEntity


class TaskLinks(LinksEntity):
    tasks: LinkEntity
    update: LinkEntity


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
