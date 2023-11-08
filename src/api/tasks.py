from fastapi import APIRouter

from api.dependencies import UOWDep
from schemas.tasks import TaskSchemaAdd, TaskSchemaEdit
from services.tasks import TasksService

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
)


@router.post("")
async def add_task(
    task: TaskSchemaAdd,
    uow: UOWDep,
):
    task_id = await TasksService().add_task(uow, task)
    return {"task_id": task_id}


@router.get("")
async def get_tasks(
    uow: UOWDep,
):
    tasks = await TasksService().get_tasks(uow)
    return tasks


@router.patch("/{task_id}")
async def edit_task(
    task_id: int,
    task: TaskSchemaEdit,
    uow: UOWDep,
):
    edited_task = await TasksService().edit_task(uow, task_id, task)
    return edited_task


@router.get("/history")
async def  get_task_history(
    uow: UOWDep
):
    task_history = await TasksService().get_task_history(uow)
    return task_history