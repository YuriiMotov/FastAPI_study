from time import sleep

from celery import Celery
from kombu import Exchange, Queue


default_exchange = Exchange('default', type='direct')
hight_priority_exchange = Exchange('hight_priority', type='direct')


celery = Celery(
    'tasks', broker='redis://localhost:6379', backend='redis://localhost:6379',
    result_extended=True,
    task_queues=(
        Queue('default', default_exchange, routing_key='default'),
        Queue('hight_priority', hight_priority_exchange, routing_key='hight_priority'),
    ),
    task_default_queue='default',
    task_default_exchange='default',
    task_default_routing_key='default'
)


@celery.task()
def celery_task1():
    sleep(1)


@celery.task(queue='hight_priority')
def celery_task2():
    sleep(1)


@celery.task()
def celery_task3():
    sleep(1)
