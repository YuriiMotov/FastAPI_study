from time import sleep

from celery import Celery


celery = Celery(
    'tasks', broker='redis://localhost:6379', backend='redis://localhost:6379',
    result_extended=True,
    broker_transport_options={
        'priority_steps': list(range(3)),
        'sep': ':',
        'queue_order_strategy': 'priority'
    }
)



@celery.task()
def celery_task1():
    sleep(1)

@celery.task()
def celery_task2():
    sleep(1)


@celery.task()
def celery_task3():
    sleep(1)
