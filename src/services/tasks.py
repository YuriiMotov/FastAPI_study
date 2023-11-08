from schemas.tasks import TaskSchema, TaskSchemaAdd, TaskSchemaEdit, TaskHistorySchemaAdd
from utils.unitofwork import IUnitOfWork


class TasksService():
    
    async def add_task(self, uow: IUnitOfWork, task: TaskSchemaAdd) -> int:
        async with uow:
            task_id = await uow.tasks.add_one(task.model_dump())
            await uow.commit()
            return task_id

    async def get_tasks(self, uow: IUnitOfWork) -> TaskSchema:
        async with uow:
            tasks = await uow.tasks.find_all()
            return tasks

    async def edit_task(
        self, uow: IUnitOfWork, task_id: int, data: TaskSchemaEdit
    ) -> TaskSchema:
        async with uow:
            current_task: TaskSchema = await uow.tasks.find_one(id=task_id)
            await uow.tasks.edit_one(task_id, data.model_dump())
            task_log = TaskHistorySchemaAdd(
                task_id=task_id,
                previous_assignee_id=current_task.assignee_id,
                new_assignee_id=data.assignee_id
            )
            await uow.task_history.add_one(task_log.model_dump())
            await uow.commit()

    async def get_task_history(self, uow: IUnitOfWork):
        async with uow:
            return await uow.task_history.find_all()

