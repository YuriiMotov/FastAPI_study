from pydantic import BaseModel


class ChatMessage(BaseModel):
    id: int
    text: str

    class Config:
        from_attributes = True