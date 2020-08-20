from src.domain.entities.user import User


class UserAuthorization:

    def __init__(self, user: User, valid_until: int):
        self.user = user
        self.valid_until = valid_until
