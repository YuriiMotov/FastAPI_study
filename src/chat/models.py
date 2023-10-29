from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from database import Base

class ChatMessage(Base):
    __tablename__ = "chat_message"
    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(String)


