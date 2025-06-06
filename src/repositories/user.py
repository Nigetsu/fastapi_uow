from src.models import User
from src.utils.repository import SqlAlchemyRepository


class UserRepository(SqlAlchemyRepository[User]):
    _model = User
