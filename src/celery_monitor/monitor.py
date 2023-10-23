import asyncio
from typing import Optional, TypeAlias, Callable

FINISHED_STATES = ('FAILURE', 'SUCCESS')
TaskErrorHandler: TypeAlias = Callable[[str, dict, Exception], None]


class CeleryTasksListNode():
    def __init__(self, task, next=None):
        self.task = task
        self.next: Optional[CeleryTasksListNode] = next


class CeleryTasksMonitor():

    def __init__(self):
        self.head: Optional[CeleryTasksListNode] = None
        self.tail: Optional[CeleryTasksListNode] = None
        self.task_failure_handlers = {}
        self.aio_task = None
        self.is_running = False
    
    def monitor_task(self, task):
        if self.head is not None:
            self.tail.next = CeleryTasksListNode(task)
        else:
            self.head = CeleryTasksListNode(task)
            self.tail = self.head
    
    def set_task_failure_handler(self, task_name: str, handler: TaskErrorHandler):
        self.task_failure_handlers[task_name] = handler

    def _on_task_failure(
        self, task_name: str, args: list, kwargs: dict, exc: Exception
    ):
        handler = self.task_failure_handlers.get(task_name)
        if handler:
            handler(task_name, args, kwargs, exc)
        else:
            print(f"Celery task {task_name} failed (default error handler): {args}, {kwargs}")
    
    def _loop_cycle(self):
            cur = self.head
            prev = None
            while cur:
                try:
                    if cur.task.state in FINISHED_STATES:
                        if cur.task.state == 'FAILURE':
                            t = cur.task
                            self._on_task_failure(t.name, t.args, t.kwargs, t.result)
                            t.forget()
                        if prev is not None:
                            prev.next = cur.next
                        else:
                            self.head = cur.next
                        if cur.next is None:
                            self.tail = prev
                    else:
                        prev = cur
                except Exception as e:
                    print(e)
                cur = cur.next

    async def loop(self):
        self.is_running = True
        while self.is_running:
            await asyncio.sleep(0)
            self._loop_cycle()

    def stop(self):
        self.is_running = False
        cur = self.head
        while cur:
            cur.task.forget()
            cur = cur.next
        self.head = None
        self.tail = None


celery_tasks_monitor = CeleryTasksMonitor()
