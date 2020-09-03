from src.domain.entities.user import User

from .base_repository import BaseRepository


class UserRepository(BaseRepository):
    def __init__(self, connection):
        super().__init__(connection, collection_name="user", entity_type=User)

    def get_user(self, filter) -> User:
        user = self._collection.find_one(filter)
        if user:
            user.update({"id": user["_id"]})
            return User(**user)

    def get_user_by_email(self, email: str) -> User:
        return self.get_user({"email": email})

    def get_user_by_name(self, username: str) -> User:
        return self.get_user({"name": username})
