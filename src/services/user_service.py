from src.domain.user import User
from src.repositories import UserRepository

import logging
logger = logging.getLogger(__name__)


class UserService:

    def __init__(self, user_repository: UserRepository):
        logger.info('INIT')
        self._user_repository = user_repository

    def get_user(self, username: str) -> User:
        pass
