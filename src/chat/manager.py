from fastapi import WebSocket
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import ChatMessage

class ChatManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(
        self, message: str, session: AsyncSession = None, add_to_db: bool = False
    ):
        if add_to_db:
            await self.add_messages_to_database(message, session)
        for connection in self.active_connections:
            await connection.send_text(message)

    @staticmethod
    async def add_messages_to_database(message: str, session: AsyncSession):
        session.add(ChatMessage(text=message))
        await session.commit()

    @staticmethod
    async def get_last_messages(session: AsyncSession) -> list[ChatMessage]:
        query = select(ChatMessage).order_by(ChatMessage.id.desc()).limit(5)
        messages = await session.execute(query)
        return reversed(messages.scalars().all())
