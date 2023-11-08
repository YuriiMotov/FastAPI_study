from models.tasks import TaskHistory
from utils.repository import SQLAlchemyRepository


class SQLATaskHistoryRepository(SQLAlchemyRepository):
    model = TaskHistory


