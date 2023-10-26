import asyncio
from httpx import AsyncClient
import pytest

from sqlalchemy import select

from conftest import client, async_session_maker
from auth.models import Role



async def add_role():
    async with async_session_maker() as session:
        session.add(Role(name="user", permissions=[]))
        await session.commit()
        roles = (await session.scalars(select(Role))).all()
        return roles[0].id
        

async def test_register(ac: AsyncClient):

    await add_role()
    response = await ac.post(
        '/auth/register',
        json={
            "email": "string",
            "password": "string",
            "is_active": True,
            "is_superuser": False,
            "is_verified": False,
            "username": "string"
        }
    )
    await asyncio.sleep(1)
    assert response.status_code == 201