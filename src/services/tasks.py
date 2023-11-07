
from schemas.tasks import TaskSchema, TaskSchemaAdd
from utils.repository import AbstractRepository


class TasksService():
    def __init__(self, tasks_repo: AbstractRepository):
        self.tasks_repo: AbstractRepository = tasks_repo
    
    async def add_task(self, task: TaskSchemaAdd) -> int:
        id = await self.tasks_repo.add_one(task.model_dump())
        return id

    async def get_tasks(self) -> TaskSchema:
        tasks = await self.tasks_repo.find_all()
        return tasks
