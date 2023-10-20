from fastapi import APIRouter, BackgroundTasks, Depends

from auth.router import fastapi_users

from .tasks import (
    long_background_task_with_exception, background_task_error_handler,
)

router = APIRouter()

