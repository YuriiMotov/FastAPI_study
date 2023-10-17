from fastapi import Depends
from fastapi_users_db_sqlalchemy import  SQLAlchemyUserDatabase
from fastapi_users_db_sqlalchemy.access_token import SQLAlchemyAccessTokenDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from .models import User, AccessToken

async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)


async def get_access_token_db(session: AsyncSession = Depends(get_async_session)):  
    yield SQLAlchemyAccessTokenDatabase(session, AccessToken)