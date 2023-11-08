from models.users import User
from utils.repository import SQLAlchemyRepository


class SQLAUsersRepository(SQLAlchemyRepository):
    model = User
