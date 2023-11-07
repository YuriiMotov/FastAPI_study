from abc import ABC, abstractmethod

from sqlalchemy import select, insert

from db.database import async_session_maker


class AbstractRepository(ABC):
    
    @abstractmethod
    async def add_one(self) -> int:
        raise NotImplementedError()

    @abstractmethod
    async def find_all(self):
        raise NotImplementedError()


class SQLAlchemyRepository(AbstractRepository):

    model = None

    async def add_one(self, data: dict) -> int:
        async with async_session_maker() as session:
            stmt = insert(self.model).values(**data).returning(self.model.id)
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one()
    
    async def find_all(self):
        async with async_session_maker() as session:
            stmt = select(self.model)
            res = await session.execute(stmt)
            res = [row[0].to_read_model() for row in res.all()]
            return res


class InMemoryRepository(AbstractRepository):
    model = None
    last_id: int = 0
    items_list: list = []

    def __init__(self):
        super().__init__()

    async def add_one(self, data: dict) -> int:
        cls = InMemoryRepository
        cls.last_id += 1
        new_item = self.model(**data)
        new_item.id = cls.last_id
        cls.items_list.append(new_item)
        return cls.last_id
    
    async def find_all(self):
        cls = InMemoryRepository
        return [item.to_read_model() for item in cls.items_list]

