from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.templating import Jinja2Templates
from fastapi_cache.decorator import cache
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from operations.router import get_specific_operations
from schemas import ErrorDetails

OPERATIONS_PER_PAGE = 3

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get('/search/{operation_type}')
async def get_search_page(
    request: Request,
    operations = Depends(get_specific_operations)
):
    return templates.TemplateResponse(
        'search.html',
        {"request": request, "operations": operations}
    )


@router.get("/chat")
async def get_chat_page(request: Request):
    return templates.TemplateResponse(
        'chat.html',
        {"request": request}
    )


@router.get("/chat-v2")
async def get_chat_v2_page(request: Request):
    return templates.TemplateResponse(
        'chat_v2.html',
        {"request": request}
    )