from fastapi import APIRouter

from .tasks import celery_task1, celery_task2, celery_task3

router = APIRouter()


@router.post(
    '/celery-tasks-with-priorities-queues',
    status_code=202
)
async def run_celery_tasks_with_priorities_queues():
    # Run 15 instances of task 1 with default priority
    for _ in range(15):
        t = celery_task1.apply_async()
        t.forget()
    # Run instance of task 2 with hight priority (set in task's declaration)
    t = celery_task2.apply_async()
    t.forget()
    # Run instance of task 3 with hight priority
    t = celery_task3.apply_async(queue='hight_priority')
    t.forget()

    # Important!
    # To make priorities work you should run at least 2 workers and one of them should
    # process only prioritized tasks:
    # celery worker -A tasks.tasks:celery -Q default,hight_priority --prefetch-multiplier=1
    # celery worker -A tasks.tasks:celery -Q hight_priority --prefetch-multiplier=1

    # It's also important to run worker with '--prefetch-multiplier=1' option. Otherwise 
    # Celery will preload (CPU_cores_count)*4 tasks from the queue by one request.
    
    # Expected result: all the instances of task_1 will be executed by worker_1.
    # Instances of task_3 and task 2 will be executed by worker_2.
    
