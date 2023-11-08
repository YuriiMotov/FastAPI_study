from fastapi import APIRouter

from api.dependencies import TasksServiceDep
from schemas.tasks import TaskSchemaAdd, TaskSchemaEdit

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
)


@router.post("")
async def add_task(
    task: TaskSchemaAdd,
    tasks_service: TasksServiceDep,
):
    task_id = await tasks_service.add_task(task)
    return {"task_id": task_id}


@router.get("")
async def get_tasks(
    tasks_service: TasksServiceDep,
):
    tasks = await tasks_service.get_tasks()
    return tasks


@router.patch("/{task_id}")
async def edit_task(
    task_id: int,
    task: TaskSchemaEdit,
    tasks_service: TasksServiceDep,
):
    edited_task = await tasks_service.edit_task(task_id, task)
    return edited_task


@router.get("/history")
async def  get_task_history(
    tasks_service: TasksServiceDep,
):
    task_history = await tasks_service.get_task_history()
    return task_history