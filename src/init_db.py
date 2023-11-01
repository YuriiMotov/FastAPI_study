import asyncio

from sqlalchemy import select

from database import async_session_maker
from auth.models import Role


async def db_init():
    async with async_session_maker() as session:
        roles = await session.scalars(select(Role))
        if len(roles.all()) == 0:
            session.add(Role(name='user'))
            session.add(Role(name='admin'))
            await session.commit()
            print("`admin` and `user` roles was added")


if __name__ == '__main__':
    asyncio.run(db_init())

