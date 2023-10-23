from celery.result import AsyncResult
from fastapi import APIRouter

from .schemas import CeleryTaskState
from .tasks import celery, celery_long_task_with_progress


router = APIRouter()


@router.post(
    '/celery-task-with-progress',
    status_code=202
)
async def run_celery_task_with_progress() -> dict[str, str]:
    t = celery_long_task_with_progress.delay()
    return {"task_id": t.id}


@router.get('/get-celery-task-progress/{task_id}')
async def get_celery_task_progress(task_id: str) -> CeleryTaskState:
    task = AsyncResult(task_id, app=celery)
    progress = 0
    if task.state == 'PROGRESS':
        progress = task.info.get('progress')
    elif task.state == 'SUCCESS':
        progress = 100
    return CeleryTaskState(task_id=task_id, state=task.state, progress=progress)
