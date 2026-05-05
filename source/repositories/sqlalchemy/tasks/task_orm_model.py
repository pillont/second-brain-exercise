from datetime import date

from sqlalchemy import Date, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from source.repositories.sqlalchemy.base_orm_model import Base


class TaskOrmModel(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), index=True)
    description: Mapped[str] = mapped_column(Text)
    due_date: Mapped[date] = mapped_column(Date, index=True)
    status: Mapped[str] = mapped_column(String(50), index=True)
