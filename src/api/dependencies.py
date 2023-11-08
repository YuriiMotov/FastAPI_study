from typing import Annotated

from fastapi import Depends

from services.tasks import TasksService
from services.users import UsersService
from utils.unitofwork import SQLAUnitOfWork, IUnitOfWork


UOWDep = Annotated[IUnitOfWork, Depends(SQLAUnitOfWork)]


async def _tasks_service(
    uow: UOWDep
) -> TasksService:
    return TasksService(uow)

async def _users_service(
    uow: UOWDep
) -> UsersService:
    return UsersService(uow)


TasksServiceDep = Annotated[TasksService, Depends(_tasks_service)]


UsersServiceDep = Annotated[UsersService, Depends(_users_service)]
