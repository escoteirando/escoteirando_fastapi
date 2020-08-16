from datetime import datetime
from hashlib import sha1
from typing import List

from password_strength import PasswordPolicy

from src.app import get_logger
from src.domain.entities.user import User
from src.domain.enums import UserMessage
from src.domain.requests import AuthSubscribeRequest
from src.domain.responses import BaseResponse, UserMenuResponse
from src.repositories import UserRepository
from src.services.mailer_service import MailerService

logger = get_logger(__name__)


class UserService:

    def __init__(self,
                 user_repository: UserRepository,
                 mailer_service: MailerService):
        logger.info('INIT')
        self._user_repository = user_repository
        self._mailer_service = mailer_service
        self._password_policy: PasswordPolicy = PasswordPolicy.from_names(
            length=5,  # min length: 8
            uppercase=1,  # need min. 2 uppercase letters
            numbers=1,  # need min. 2 digits
            special=1,  # need min. 2 special characters
            # need min. 2 non-letter characters (digits, specials, anything)
            nonletters=1,
        )

    def create_user(
            self,
            user_request: AuthSubscribeRequest) -> BaseResponse:
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
            errors.append("Senha não atende os padrões de complexidade")

        if errors:
            return BaseResponse(ok=False,
                                msg=str(errors))

        user = User(id=0,
                    name=user_request.username,
                    email=user_request.email,
                    ueb_id=0,
                    active=False,
                    password_hash=self._password_hash(user_request.password),
                    creation_date=datetime.now(),
                    validated=False)
        if self._user_repository.save(user):
            # TODO: Enviar email de validação do usuário
            return BaseResponse(ok=True,
                                msg="Usuário criado com sucesso")

        return BaseResponse(ok=False,
                            msg="Erro na gravação do usuário")

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
        return self._password_policy.test(password)

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

    def get_user(self, username_email: str) -> User:
        user = self.get_user_by_name(username_email)
        if not user:
            user = self.get_user_by_email(username_email)
        return user

    def get_user_menu(self, user: User) -> List[UserMenuResponse]:
        return [
            UserMenuResponse(id=999, text='Sair',
                             route='/auth/logout', icon='mdi-exit-to-app')
        ]
