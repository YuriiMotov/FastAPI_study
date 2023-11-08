from abc import ABC, abstractmethod
from typing import Type

from db.database import async_session_maker
from repositories.tasks import TasksRepository
from repositories.task_history import TaskHistoryRepository
from repositories.users import UsersRepository


class IUnitOfWork(ABC):
    tasks: Type[TasksRepository]
    task_history: Type[TaskHistoryRepository]
    users: Type[UsersRepository]

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


class UnitOfWork():

    def __init__(self):
        self.session_factory = async_session_maker

    async def __aenter__(self):
        self.session = self.session_factory()
        self.tasks = TasksRepository(self.session)
        self.task_history = TaskHistoryRepository(self.session)
        self.users = UsersRepository(self.session)

    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()