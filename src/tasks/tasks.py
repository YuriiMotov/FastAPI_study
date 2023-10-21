from time import sleep

from celery import Celery

celery = Celery(
    'tasks', broker='redis://localhost:6379', backend='redis://localhost:6379'
)


@celery.task(bind=True)
def long_celery_task_with_exception(param1: str, *args, **kwargs):
    sleep(5)
    raise Exception("Some information about error")

