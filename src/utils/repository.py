from abc import ABC, abstractmethod

from sqlalchemy import select, insert, update
from sqlalchemy.ext.asyncio import AsyncSession


class AbstractRepository(ABC):
    
    @abstractmethod
    async def add_one(self) -> int:
        raise NotImplementedError()

    @abstractmethod
    async def find_all(self):
        raise NotImplementedError()


class SQLAlchemyRepository(AbstractRepository):

    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_one(self, data: dict) -> int:
        stmt = insert(self.model).values(**data).returning(self.model.id)
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def edit_one(self, id: int, data: dict):
        st = update(self.model).values(**data).filter_by(id=id) \
                .returning(self.model.id)
        res = await self.session.execute(st)
        return res.scalar_one()

    async def find_one(self, **filter_by):
        st = select(self.model).filter_by(**filter_by)
        res = await self.session.execute(st)
        return res.scalar_one().to_read_model()

    async def find_all(self):
        stmt = select(self.model)
        res = await self.session.execute(stmt)
        res = [row[0].to_read_model() for row in res.all()]
        return res



