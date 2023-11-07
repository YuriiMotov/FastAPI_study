from models.tasks import Task
from utils.repository import SQLAlchemyRepository, InMemoryRepository


class TasksRepository(SQLAlchemyRepository):
    model = Task

class TasksInMemoryRepository(InMemoryRepository):
    model = Task