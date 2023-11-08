from schemas.users import UserSchemaAdd
from utils.unitofwork import IUnitOfWork


class UsersService:

    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def add_user(self, user: UserSchemaAdd):
        async with self.uow:
            user_id = await self.uow.users.add_one(user.model_dump())
            await self.uow.commit()
            return user_id

    async def get_users(self):
        async with self.uow:
            users = await self.uow.users.find_all()
            return users