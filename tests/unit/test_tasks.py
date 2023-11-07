import pytest

from services.tasks import TasksService
from schemas.tasks import TaskSchema, TaskSchemaAdd
from repositories.tasks import TasksInMemoryRepository


@pytest.fixture()
def tasks_service():
    return TasksService(TasksInMemoryRepository())


async def test_add_task(tasks_service: TasksService):
    task = TaskSchemaAdd(
        title="Write tests",
        author_id=0,
        assignee_id=0
    )
    id = await tasks_service.add_task(task)
    assert id is not None
    assert len(TasksInMemoryRepository.items_list) > 0
    tasks = [task for task in TasksInMemoryRepository.items_list if task.id == id]
    assert len(tasks) == 1


async def test_get_tasks(tasks_service: TasksService):
    task = TaskSchemaAdd(
        title="Write tests",
        author_id=0,
        assignee_id=0
    )
    await tasks_service.add_task(task)
    
    tasks = await tasks_service.get_tasks()
    assert len(tasks) > 0
    assert isinstance(tasks[0], TaskSchema)