from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy import select

from database import AsyncSession, async_session_maker, get_async_session
from .manager import ConnectionManager
from .models import ChatMessage
from .schemas import MessagesModel

router = APIRouter()


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str, add_to_db: bool):
        if add_to_db:
            await self.add_messages_to_database(message)
        for connection in self.active_connections:
            await connection.send_text(message)

    @staticmethod
    async def add_messages_to_database(message: str):
        async with async_session_maker() as session:
            session.add(ChatMessage(text=message))
            await session.commit()


chat_manager = ConnectionManager()


@router.get("/last_messages")
async def get_last_messages(
        session: AsyncSession = Depends(get_async_session),
) -> list[MessagesModel]:
    query = select(ChatMessage).order_by(ChatMessage.id.desc()).limit(5)
    messages = await session.execute(query)
    return messages.scalars().all()


@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await chat_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await chat_manager.broadcast(f"#{client_id} says: {data}", add_to_db=True)
    except WebSocketDisconnect:
        chat_manager.disconnect(websocket)
        await chat_manager.broadcast(f"#{client_id} left the chat", add_to_db=False)
