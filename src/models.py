from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class OAuth2User(Base):
    __tablename__ = "oauth2_user"
    id: Mapped[int] = mapped_column(
        primary_key=True
    )
    username: Mapped[str] = mapped_column(
        String(30), nullable=False
    )
    fullname: Mapped[str] = mapped_column(
        String(60), nullable=False
    )
    email: Mapped[str] = mapped_column(
        String(length=320), unique=True, index=True, nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(
        String(length=1024), nullable=False
    )
    disabled: Mapped[bool] = mapped_column(
        Boolean, default=True, nullable=False
    )
    scopes: Mapped[str] = mapped_column(nullable=True, default='')

    