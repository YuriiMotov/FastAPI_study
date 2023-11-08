from models.tasks import Task
from utils.repository import SQLAlchemyRepository


class SQLATasksRepository(SQLAlchemyRepository):
    model = Task