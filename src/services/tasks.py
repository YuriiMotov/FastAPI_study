from schemas.tasks import TaskSchema, TaskSchemaAdd, TaskSchemaEdit, TaskHistorySchemaAdd
from utils.unitofwork import IUnitOfWork


class TasksService():

    def __init__(self, uow: IUnitOfWork):
        self.uow = uow
    
    async def add_task(self, task: TaskSchemaAdd) -> int:
        async with self.uow:
            task_id = await self.uow.tasks.add_one(task.model_dump())
            await self.uow.commit()
            return task_id

    async def get_tasks(self) -> TaskSchema:
        async with self.uow:
            tasks = await self.uow.tasks.find_all()
            return tasks

    async def edit_task(
        self, task_id: int, data: TaskSchemaEdit
    ) -> TaskSchema:
        async with self.uow:
            current_task: TaskSchema = await self.uow.tasks.find_one(id=task_id)
            await self.uow.tasks.edit_one(task_id, data.model_dump())
            task_log = TaskHistorySchemaAdd(
                task_id=task_id,
                previous_assignee_id=current_task.assignee_id,
                new_assignee_id=data.assignee_id
            )
            await self.uow.task_history.add_one(task_log.model_dump())
            await self.uow.commit()

    async def get_task_history(self):
        async with self.uow:
            return await self.uow.task_history.find_all()

