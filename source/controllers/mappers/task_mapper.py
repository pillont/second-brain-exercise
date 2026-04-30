from source.controllers.entities.list_entity import ListEntity
from source.controllers.mappers.list_entity_mapper import map_to_list_entity
from source.models.filtered_list import FilteredList
from source.models.task import Task, TaskData, TaskUpdateData
from source.controllers.entities.task_entity import (
    TaskDataEntity,
    TaskEntity,
    TaskLinks,
    TaskUpdateDataEntity,
)
from source.controllers.entities.link import HttpMethod, LinkEntity


def to_task_data(entity: TaskDataEntity) -> TaskData:
    return TaskData(
        title=entity["title"],
        description=entity["description"],
        due_date=entity["due_date"],
    )


def to_task_update_data(entity: TaskUpdateDataEntity) -> TaskUpdateData:
    return TaskUpdateData(
        title=entity["title"],
        description=entity["description"],
        due_date=entity["due_date"],
        status=entity["status"],
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


def map_to_filtered_tasks_list(all_tasks: FilteredList[Task]) -> ListEntity[TaskEntity]:
    return map_to_list_entity(
        FilteredList(
            (to_task_entity(t) for t in all_tasks.elements), has_next=all_tasks.has_next
        )
    )


def _build_links(task: Task) -> TaskLinks:
    return TaskLinks(
        self_link=LinkEntity(href=f"/tasks/{task.id}"),
        tasks=LinkEntity(href="/tasks/"),
        update=LinkEntity(href=f"/tasks/{task.id}", type=HttpMethod.PUT),
        delete=LinkEntity(href=f"/tasks/{task.id}", type=HttpMethod.DELETE),
    )
