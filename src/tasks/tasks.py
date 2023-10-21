from time import sleep

from celery import Celery
from celery.signals import task_failure

celery = Celery(
    'tasks', broker='redis://localhost:6379', backend='redis://localhost:6379'
)


class MonitoredTask(celery.Task):
    def on_failure(self, exc, task_id, args: list, kwargs: dict, einfo):
        arguments = ', '.join(args + list(map(lambda k, v: f'{k}={v}', kwargs.items())))
        print(
            f"BaseClass: Celery task {self.name} with arguments ({arguments}) failed: " \
            f"{exc.__class__}({exc})"
        )


@celery.task(bind=True, base=MonitoredTask)
def long_celery_task_with_exception(param1: str, *args, **kwargs):
    sleep(5)
    raise Exception("Some information about error")


@task_failure.connect()
def on_task_failure(
    sender, task_id, exception, args, kwargs, traceback, einfo, **allkwargs
):
    arguments = ', '.join(args + list(map(lambda k, v: f'{k}={v}', kwargs.items())))
    print(
        f"Signals: Celery task {sender.name} with arguments ({arguments}) failed: " \
        f"{exception.__class__}({exception})"
    )
