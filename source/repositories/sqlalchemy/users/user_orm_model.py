
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from source.repositories.sqlalchemy.base_orm_model import Base


class UserOrmModel(Base):
    __tablename__ = "authent"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    username: Mapped[str] = mapped_column(String(255), index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
