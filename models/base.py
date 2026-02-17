from typing import Any

from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column

from core.db import db


class Base(db.Model):  # раз есть db.Model, значит это не обычный python класс. Это модель для Базы Данных
    __abstract__ = True

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    def to_dict(self) -> dict[str, Any]:
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }

    # User -> User.to_dict() => => {"id": 1, "name": "Vasya", ...}
