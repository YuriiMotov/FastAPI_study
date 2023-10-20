import asyncio
from typing import Callable, TypeAlias

from celery import Celery

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465

celery = Celery('tasks', broker='redis://localhost:6379')

