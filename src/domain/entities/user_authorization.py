from src.domain.entities.user import User


class UserAuthorization:
    """ Classe utilizada pelo middleware de autorização
    para manter o usuário logado até o período de validade """

    def __init__(self, user: User, valid_until: int):
        self.user = user
        self.valid_until = valid_until
