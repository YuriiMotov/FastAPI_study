from celery import Celery

celery = Celery(
    'tasks', broker='redis://localhost:6379', backend='redis://localhost:6379',
    result_extended=True
)

