from dataclasses import dataclass
from datetime import date
from typing import Optional

from source.models.task import TaskStatus

@dataclass
class TaskFilters:
    status: Optional[TaskStatus] = None
    due_date_from: Optional[date] = None
    due_date_to: Optional[date] = None
    title: Optional[str] = None
