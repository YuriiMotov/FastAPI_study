from sqlalchemy import select

from conftest import client, async_session_maker
from auth.models import Role


async def test_add_role():
    async with async_session_maker() as session:
        session.add(Role(name="user", permissions=[]))
        await session.commit()

        roles = (await session.scalars(select(Role))).all()
        assert len(roles) == 1
        assert roles[0].id == 1
        assert roles[0].name == 'user'
        assert roles[0].permissions == []
        

def test_register():
    response = client.post(
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

    assert response.status_code == 201