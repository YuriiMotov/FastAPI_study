from abc import ABC, abstractmethod

from db.database import async_session_maker
from repositories.tasks import SQLATasksRepository
from repositories.task_history import SQLATaskHistoryRepository
from repositories.users import SQLAUsersRepository
from utils.repository import AbstractRepository


class IUnitOfWork(ABC):
    tasks: AbstractRepository
    task_history: AbstractRepository
    users: AbstractRepository

    @abstractmethod
    async def __aenter__(self):
        raise NotImplementedError

    @abstractmethod
    async def __aexit__(self, *args):
        raise NotImplementedError
    
    @abstractmethod
    async def commit(self):
        raise NotImplementedError

    @abstractmethod
    async def rollback(self):
        raise NotImplementedError


class SQLAUnitOfWork():

    def __init__(self):
        self.session_factory = async_session_maker

    async def __aenter__(self):
        self.session = self.session_factory()
        self.tasks = SQLATasksRepository(self.session)
        self.task_history = SQLATaskHistoryRepository(self.session)
        self.users = SQLAUsersRepository(self.session)

    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()