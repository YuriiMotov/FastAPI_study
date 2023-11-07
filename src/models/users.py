from sqlalchemy.orm import Mapped, mapped_column

from db.database import Base
from schemas.users import UserSchema


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

    def to_read_model(self) -> UserSchema:
        return UserSchema(
            id=self.id, 
            name=self.name,
        )