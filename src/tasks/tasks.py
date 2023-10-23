from time import sleep

from celery import Celery

RESULT_EXPIRE_TIME = 60*60*12   # After this time Celery will remove results. Celery beat
                                # has to be run to do that

celery = Celery(
    'tasks', broker='redis://localhost:6379', backend='redis://localhost:6379',
    result_extended=True,   
    result_expires=RESULT_EXPIRE_TIME
)


@celery.task(bind=True)
def celery_long_task_with_progress(self):

    TOTAL_STEPS = 10

    for step in range(TOTAL_STEPS):
        progress = (step * 100) // TOTAL_STEPS
        self.update_state(state='PROGRESS', meta={'progress': progress})
        sleep(3)
