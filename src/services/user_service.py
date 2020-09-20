from datetime import datetime
from hashlib import sha1
from typing import List

from src.app import get_logger
from src.domain.entities.user import User
from src.domain.enums import UserLevel
from src.domain.requests import (AuthSubscribeRequest, UserProfileRequest,
                                 UserSetPasswordRequest)
from src.domain.responses import (BaseResponse, UserHomeCardResponse,
                                  UserMenuResponse)
from src.repositories import UserRepository
from src.services.user.user_validation_service import UserValidationService

logger = get_logger(__name__)

user_validation = UserValidationService.Instance()


class UserService:
    def __init__(self, user_repository: UserRepository):
        logger.info("INIT")
        self._user_repository = user_repository

    def create_user(self, user_request: AuthSubscribeRequest) -> BaseResponse:
        errors = []
        success, msg = user_validation.is_valid_username(user_request.username)
        if not success:
            errors.append(msg)

        success, msg = user_validation.is_valid_email(user_request.email)
        if not success:
            errors.append(msg)
        else:
            user = self._user_repository.get_user_by_email(user_request.email)
            if user:
                errors.append("Email já foi registrado por um usuário")

        success, msg = user_validation.is_valid_password(user_request.password)
        if not success:
            errors.append(msg)

        if errors:
            return BaseResponse(ok=False, msg=str(errors))

        user = User(
            id=0,
            name=user_request.username,
            email=user_request.email,
            ueb_id=0,
            active=False,
            password_hash=self._password_hash(user_request.password),
            creation_date=datetime.now(),
            validated=False,
            mappa_valid_until=0
        )
        if self._user_repository.save(user):
            # TODO: Enviar email de validação do usuário
            return BaseResponse(ok=True, msg="Usuário criado com sucesso")

        return BaseResponse(ok=False, msg="Erro na gravação do usuário")

    def save_user(self, user: User) -> bool:
        return self._user_repository.save(user)

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
            password = ""
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
        menus = []
        menus.append(
            UserMenuResponse(
                id=1, text="Perfil",
                route="/api/user/profile", icon="mdi-person"
            )
        )
        if not user.mappa_user:
            menus.append(
                UserMenuResponse(
                    id=888, text="Credenciais mAPPa",
                    route="/auth/mappa")
            )

        menus.append(
            UserMenuResponse(
                id=999, text="Sair",
                route="/auth/logout", icon="mdi-exit-to-app"
            )
        )
        return menus

    def set_password(
        self, user: User, password_request: UserSetPasswordRequest
    ) -> (bool, str):
        command_user = user
        if user.email == password_request.email:
            updated_user = user
        elif user.level is UserLevel.normal:
            logger.warning(
                "PASSWORD SETTING FROM NON-ADMIN USER DENIED: %s",
                command_user.email)
            return False, "Usuário sem permissão para alterar outro usuário"
        else:
            updated_user = self.get_user_by_email(password_request.email)
            if not updated_user:
                logger.warning(
                    "PASSWORD SETTING FOR NOT FOUND USER: %s - CALLED BY %s",
                    password_request.email,
                    command_user.email,
                )
                return False, "Usuário não encontrado"

        password_restrictions = self.password_restrictions(
            password_request.password)
        if password_restrictions:
            logger.warning(
                "PASSWORD SETTING NOT SET FOR USER %s: %s - CALLED BY %s",
                password_request.email,
                password_restrictions,
                command_user.email,
            )
            return False, "Senha não atende padrão de complexidade"

        updated_user.password_hash = self._password_hash(
            password_request.password)
        if not self.save_user(updated_user):
            logger.warning(
                "CANNOT SAVE USER %s FOR NEW PASSWORD - CALLED BY %s",
                password_request.email,
                command_user.email,
            )
            return False, "Erro ao gravar usuário"

        logger.info(
            "PASSWORD UPDATED FOR USER %s - CALLED BY %s",
            password_request.email,
            command_user.email,
        )
        return True, "Senha atualizada com sucesso"

    def get_user_home_cards(self, user: User):
        cards = []
        if user.mappa_user:
            cards.append(
                UserHomeCardResponse(
                    title="Minha seção",
                    route="mappa_secao",
                    subtitle="Informações sobre a seção",
                )
            )
        cards.append(
            UserHomeCardResponse(
                title="Atividades",
                route="atividades",
                subtitle="Navegação por atividades",
            )
        )
        cards.append(
            UserHomeCardResponse(
                title="Encontros",
                route="encontros",
                subtitle="Navegação por encontros"
            )

        )
        cards.append(
            UserHomeCardResponse(
                title="Perfil", route="profile", subtitle="Minhas informações"
            )
        )

        return cards

    def save_profile(self, user: User, profile: UserProfileRequest) -> str:
        """Grava o perfil do usuário. Retorna vazio se sucesso.
        Caso contrário retorna motivo da falha"""
        user2: User = None if not profile.mappa_user else\
            self._user_repository.get_user_by_mappa(profile.mappa_user)
        if user2 and user2.id != user.id:
            return f"Usuário mAPPa '{profile.mappa_user}' está em uso por outro usuário"

        email_valido, motivo = user_validation.is_valid_email(profile.email)
        if not email_valido:
            return motivo

        user2 = self.get_user_by_email(profile.email)
        if user2 and user2.id != user.id:
            return f"Email {profile.email} está em uso por outro usuário"

        user.mappa_user = profile.mappa_user
        user.full_name = profile.name
        user.email = profile.email
        user.nascimento = profile.nascimento
        user.sexo = profile.sexo
        user.ramo = profile.ramo

        return "" if self.save_user(user) else "Erro na gravação do usuário"
