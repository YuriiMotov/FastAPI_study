from fastapi import APIRouter

from .tasks import celery_task1, celery_task2, celery_task3

router = APIRouter()


@router.post(
    '/celery-tasks-with-priorities-redis',
    status_code=202
)
async def run_celery_tasks_with_priorities_redis():
    # Run 15 exemplars of task 1 with low priority
    for _ in range(15):
        t = celery_task1.apply_async(priority=2)
        t.forget()
    # Run exemplar of task 2 with low priority
    t = celery_task2.apply_async(priority=2)
    t.forget()
    # Run exemplar of task 3 with hight priority
    t = celery_task3.apply_async(priority=0)
    t.forget()

    # Expected result: task_3 will be executed before task_2, task_2 will be executed
    # after all instances of task_1
    
    # !! It's important to run worker with '--prefetch-multiplier=1' option. Otherwise 
    # Celery will preload (CPU_cores_count)*4 tasks from the queue by one request.
