from source.models.task import Task, TaskData, TaskStatus
from source.repositories.sqlalchemy.tasks.task_orm_model import TaskOrmModel


def to_orm_task(task_data: TaskData) -> TaskOrmModel:
    return TaskOrmModel(
        title=task_data.title,
        description=task_data.description,
        due_date=task_data.due_date,
        status=str(TaskStatus.INCOMPLETE),
    )


def to_task(orm_task: TaskOrmModel) -> Task:
    return Task(
        id=orm_task.id,
        title=orm_task.title,
        description=orm_task.description,
        due_date=orm_task.due_date,
        status=TaskStatus(orm_task.status),
    )
