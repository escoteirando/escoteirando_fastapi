from datetime import datetime, timedelta
from uuid import uuid1

from cache_gs import CacheGS
from src.app import get_logger, Config
from src.domain.entities.user import User
from src.domain.enums import UserLevel
from src.domain.requests import (AuthPasswordRedefineRequest,
                                 UserSetPasswordRequest)
from src.services.mailer_service import MailerService
from src.services.user.user_validation_service import UserValidationService
from src.services.user_service import UserService

logger = get_logger(__name__)
validation_service = UserValidationService.Instance()


class UserPasswordService:

    def __init__(self,
                 cache,
                 user_service: UserService,
                 mailer: MailerService):

        self._cache: CacheGS = cache
        self._user_service = user_service
        self._mailer = mailer
        self._validade_chave = timedelta(hours=6)
        self._config = Config()

    def send_password_reset_email(self, username_email: str):
        user: User = self._user_service.get_user(username_email)
        if not user:
            logger.warning(
                'PASSWORD RESET REQUEST FOR NOT FOUND USER: %s',
                username_email)
            return

        auth = str(uuid1()).replace('-', '')

        if not self._cache.set_value('pwd', auth, user.email,
                                     self._validade_chave.total_seconds):
            logger.warning('CANNOT SET PASSWORD KEY FOR USER: %s',
                           user.email)
            return
        logger.info('PASSWORD RESET REQUEST: %s - %s', user.email, auth)
        body = """Você solicitou a redefinição de sua senha no portal Escoteirando.org.

Clique no link abaixo para continuar:
{0}:{1}/f#/auth/redefine?chave={2}

Esta chave será válida até {3}
""".format(self._config.BACKEND_HOST,
           self._config.FRONTEND_PORT,
           auth,
           (datetime.now()+self._validade_chave).strftime('%d/%m/%Y %H:%M'))
        self._mailer.send(
            user.email, "[ESCOTEIRANDO] REDEFINIÇÃO DE SENHA", body)

    def validate_password_reset_key(self, key) -> User:
        user_email = self._cache.get_value('pwd', key, '0')
        if not user_email:
            return None
        user = self._user_service.get_user(user_email)
        return user

    def redefine_password(self,
                          password_redefine: AuthPasswordRedefineRequest) -> (bool, str):
        user: User = self.validate_password_reset_key(
            password_redefine.authorization)
        if not user:
            return False, 'Chave inválida ou expirada'
        if user.email != password_redefine.email:
            return False, 'Chave não corresponde ao e-mail informado'
        success, msg = validation_service.is_valid_password(
            password_redefine.password)
        if not success:
            return success, msg

        user.password_hash = UserService._password_hash(
            password_redefine.password)
        if not self._user_service.save_user(user):
            logger.warning('CANNOT SAVE USER %s FOR NEW PASSWORD',
                           password_redefine.email)
            return False, "Erro ao gravar usuário"

        logger.info('PASSWORD UPDATED FOR USER %s',
                    password_redefine.email)
        self._cache.delete_value('pwd', password_redefine.key)
        return True, "Senha atualizada com sucesso"

    def set_password(self, user: User,
                     password_request: UserSetPasswordRequest) -> (bool, str):
        command_user = user
        if user.email == password_request.email:
            updated_user = user
        elif user.level is UserLevel.normal:
            logger.warning(
                'PASSWORD SETTING FROM NON-ADMIN USER DENIED: %s',
                command_user.email)
            return False, "Usuário sem permissão para alterar outro usuário"
        else:
            updated_user = self.get_user_by_email(password_request.email)
            if not updated_user:
                logger.warning(
                    'PASSWORD SETTING FOR NOT FOUND USER: %s - CALLED BY %s',
                    password_request.email,
                    command_user.email)
                return False, "Usuário não encontrado"

        password_restrictions = self.password_restrictions(
            password_request.password)
        if password_restrictions:
            logger.warning('PASSWORD SETTING NOT SET FOR USER %s: %s - CALLED BY %s',
                           password_request.email,
                           password_restrictions,
                           command_user.email)
            return False, "Senha não atende padrão de complexidade"

        updated_user.password_hash = self._password_hash(
            password_request.password)
        if not self.save_user(updated_user):
            logger.warning('CANNOT SAVE USER %s FOR NEW PASSWORD - CALLED BY %s',
                           password_request.email,
                           command_user.email)
            return False, "Erro ao gravar usuário"

        logger.info('PASSWORD UPDATED FOR USER %s - CALLED BY %s',
                    password_request.email,
                    command_user.email)
        return True, "Senha atualizada com sucesso"
