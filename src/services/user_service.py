from src.domain.entities.user import User
from src.repositories import UserRepository
from src.domain.requests import AuthSubscribeRequest
from src.domain.responses import AuthSubscribeResponse
import logging
from src.services.mailer_service import MailerService
from hashlib import sha1

logger = logging.getLogger(__name__)


class UserService:

    def __init__(self,
                 user_repository: UserRepository,
                 mailer_service: MailerService):
        logger.info('INIT')
        self._user_repository = user_repository
        self._mailer_service = mailer_service

    def create_user(
            self,
            user_request: AuthSubscribeRequest) -> AuthSubscribeResponse:
        errors = []
        if not user_request.username:
            errors.append("Usuário não informado")
        elif not self.is_valid_username(user_request.username):
            errors.append("Usuário contém caracteres inválidos")
        if not user_request.email:
            errors.append("Email não informado")
        elif not self._mailer_service.is_valid_email(user_request.email):
            errors.append("Email inválido")
        else:
            user = self._user_repository.get_user_by_email(user_request.email)
            if user:
                errors.append("Email já foi registrado por um usuário")
        if not user_request.password:
            errors.append("Senha não foi informada")
        elif self.password_restrictions(user_request.password):
            errors.append("Senha não atende os padrões de complexidade [")
            # TODO: Implementar password_restrictions
        if errors:
            return AuthSubscribeResponse(success=False,
                                         message=str(errors))

        user = User(id=0,
                    name=user_request.username,
                    email=user_request.email,
                    ueb_id=0,
                    active=False,
                    password_hash='')
        if self._user_repository.save(user):
            return AuthSubscribeResponse(success=True,
                                         message="Usuário criado")

        return AuthSubscribeResponse(success=False,
                                     message="Não foi possível criar o usuário")

    def is_valid_username(self, username) -> bool:
        """ Username validation:

        * Characters allowed: [a-zA-z0-9.-_]
        """
        if not (8 <= len(username) <= 20):
            # Length: 8 to 20
            return False

        for c in username:
            if ('A' <= c <= 'Z' or
                'a' <= c <= 'z' or
                '0' <= c <= '9' or
                    c in ['_', '-', '.']):
                continue
            return False

        return True

    def password_restrictions(self, password: str) -> str:
        """
        Deve retornar vazio se a senha estiver OK.
        Caso contrário, deve retornar o problema com a senha
        """
        # TODO: Implementar password_restrictions
        return ""

    def is_valid_password(self, user: User, password: str) -> bool:
        return self._password_hash(password) == user.password_hash

    @staticmethod
    def _password_hash(password: str) -> str:
        if not isinstance(password, str):
            password = ''
        return sha1(str.encode(password)).hexdigest()

    def get_user_by_name(self, username: str) -> User:
        return self._user_repository.get_user_by_name(username)

    def get_user_by_email(self, email: str) -> User:
        return self._user_repository.get_user_by_email(email)
