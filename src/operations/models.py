from sqlalchemy import TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


DEFAULT_USER_ROLE = 1


class Operation(Base):
    __tablename__ = "operation"
    id: Mapped[int] = mapped_column(primary_key=True)
    quantity: Mapped[str] = mapped_column(nullable=False)
    figi: Mapped[str] = mapped_column(nullable=False)
    instrument_type: Mapped[str] = mapped_column(nullable=True)
    date: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, nullable=False)
    type: Mapped[str] = mapped_column(nullable=False)

    def update_from_dict(self, data: dict):
        for attr, val in data.items():
            if val is not None:
                self.__setattr__(attr, val)


