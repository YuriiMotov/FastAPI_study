from fastapi import APIRouter, BackgroundTasks, Depends

from auth.router import fastapi_users

from .tasks import (
    long_background_task_with_exception, background_task_error_handler,
)

router = APIRouter()

# Long operation in the background with the result's checking (FastAPI BackgroundTasks)
@router.get(
    '/long-operation-fastapi-bg-check',
    status_code=202
)
async def long_operation_fastapi_bg_with_result_checking(
    background_tasks: BackgroundTasks
):
    background_tasks.add_task(
        long_background_task_with_exception,
        "parameter value",
        background_task_error_handler
    )
