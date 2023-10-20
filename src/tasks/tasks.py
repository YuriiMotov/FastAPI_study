import asyncio
from typing import Callable, TypeAlias

from celery import Celery

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465

celery = Celery('tasks', broker='redis://localhost:6379')

CallbackHandler: TypeAlias = Callable[[str, dict, Exception], None]


async def background_task_error_handler(
    task_name: str, task_params: dict, exc: Exception
):
    print(
        f"Exception during the execution of task `{task_name}` " \
        f"with parameters ({task_params}): {exc.__class__}({exc})"
    )


async def long_background_task_with_exception(param1: str, error_callback: CallbackHandler):
    try:
        await asyncio.sleep(2)
        raise Exception("Some information about error")
    except Exception as e:
        await error_callback(
            'long_background_task_with_exception', {'param1': param1}, e
        )
