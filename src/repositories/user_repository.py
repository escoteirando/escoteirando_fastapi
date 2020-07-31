from src.domain.entities.user import User

from .base_repository import BaseRepository


class UserRepository(BaseRepository):

    def __init__(self, connection):
        super().__init__(connection,
                         collection_name="user",
                         entity_type=User)

    def get_user_by_email(self, email: str) -> User:
        user = self._collection.find_one({"email": email})
        if user:
            return User(user)
