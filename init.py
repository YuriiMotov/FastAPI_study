import asyncio

from sqlalchemy import text

from auth.database import async_session_maker

# from models.models import Role


# async def main():
#     async with async_session_maker() as session:
#         r = Role(name='user', permissions=[])

#         session.add(r)
#         await session.commit()



async def main2():
    async with async_session_maker() as session:
        await session.execute(text("INSERT INTO role (id, name, permissions) VALUES (1, 'user', '[]')"))
        await session.commit()

        # res = await session.execute(text("SELECT * FROM role"))
        # for r in res.all():
        #     print(r)




if __name__ == '__main__':
    asyncio.run(main2())