from source.models.task import Task, TaskData
from source.controllers.entities.task_entity import TaskDataEntity, TaskEntity, TaskLinks
from source.controllers.entities.link import Link, Links


def to_task_data(entity: TaskDataEntity) -> TaskData:
    return TaskData(
        title=entity.title,
        description=entity.description,
        due_date=entity.due_date,
    )


def _build_links(task: Task) -> TaskLinks:
    return TaskLinks(
        self_link=Link(href=f"/tasks/{task.id}"),
        tasks= Link(href="/tasks/")
    )


def to_task_entity(task: Task) -> TaskEntity:
    links = _build_links(task)
    return TaskEntity(
        id=task.id,
        title=task.title,
        description=task.description,
        due_date=task.due_date,
        status=task.status,
        links=links,
    )
