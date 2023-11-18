from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy import select

from database import AsyncSession, async_session_maker, get_async_session
from .manager import ChatManager
from .schemas import ChatMessage

router = APIRouter()

chat_manager = ChatManager()


@router.get("/last-messages")
async def get_last_messages(
        session: AsyncSession = Depends(get_async_session),
) -> list[ChatMessage]:
    return await chat_manager.get_last_messages(session)


@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await chat_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            async with async_session_maker() as session:
                await chat_manager.broadcast(
                    f"#{client_id} says: {data}", session=session, add_to_db=True
                )
    except WebSocketDisconnect:
        chat_manager.disconnect(websocket)
        await chat_manager.broadcast(f"#{client_id} left the chat")
