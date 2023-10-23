from fastapi import APIRouter

from .tasks import long_celery_task_with_exception
from celery_monitor.monitor import celery_tasks_monitor


router = APIRouter()

# Long operation in the background with the result's checking (Celery)
@router.get(
    '/long-operation-celery-check',
    status_code=202
)
async def long_operation_celery_with_result_checking():
    t = long_celery_task_with_exception.delay("parameter value")
    celery_tasks_monitor.monitor_task(t)


