import time
import uuid

from src.app import get_logger
from src.domain.entities.user import User
from src.domain.entities.user_authorization import UserAuthorization
from src.domain.responses import AuthLoginResponse
from src.domain.responses.user_data_response import UserDataResponse

logger = get_logger(__name__)


class AuthorizationService:

    CACHE_SECTION = "_auth"

    def __init__(self, cache_service, user_service, config):
        logger.info("INIT")
        self._cache = cache_service
        self._user_service = user_service
        self._config = config

    def _auth_key(self, key: str) -> str:
        return f"auth_{key}"

    def create_authorizaton(self, user: User) -> str:
        new_auth = str(uuid.uuid1())
        user_auth = (user.dict(), time.time() + self._config.AUTHORIZATION_TTL)

        if self._cache.set_value(
            self.CACHE_SECTION,
            self._auth_key(new_auth),
            user_auth,
            self._config.AUTHORIZATION_TTL,
        ):
            return new_auth

    def user_from_authorization(self, authorization: str) -> UserAuthorization:
        obj = self._cache.get_value(
            self.CACHE_SECTION, self._auth_key(authorization))
        if obj:
            user, valid_until = obj
            user = User.construct(**user)
        else:
            valid_until = 0
            user = None
        return UserAuthorization(user, valid_until)

    def login(self, username: str, password: str) -> AuthLoginResponse:
        user: User = self._user_service.get_user(username)
        if not user:
            return AuthLoginResponse(message="Usuário não encontrado")

        if not self._user_service.is_valid_password(user, password):
            return AuthLoginResponse(message="Senha inválida")

        if not user.active:
            return AuthLoginResponse(message="User is inactive")

        valid_until = time.time() + self._config.AUTHORIZATION_TTL
        auth = self.create_authorizaton(user)
        if not auth:
            return AuthLoginResponse(
                authorization=None,
                message="Authorization engine failed",
                valid_until=0
            )
        user_response = UserDataResponse(
            id=user.id,
            name=user.name,
            email=user.email,
            ueb_id=user.ueb_id,
            mappa_user=user.mappa_user or "",
            full_name=user.full_name,
            nascimento=user.nascimento,
            mappa_auth=user.mappa_auth,
            mappa_valid_until=user.mappa_valid_until,
            sexo=user.sexo
        )
        return AuthLoginResponse(
            authorization=auth,
            message="Authorized",
            validUntil=valid_until,
            user=user_response,
        )

    def get_authorization_data(self, authorization: str) -> AuthLoginResponse:
        user_authorization: UserAuthorization = self.user_from_authorization(
            authorization
        )

        user = user_authorization.user
        valid_until = user_authorization.valid_until

        if user_authorization.user:
            return AuthLoginResponse(
                authorization=authorization,
                user=UserDataResponse(
                    id=user.id,
                    name=user.name,
                    email=user.email,
                    ueb_id=user.ueb_id or 0,
                    mappa_user=user.mappa_user or "",
                    full_name=user.full_name,
                    nascimento=user.nascimento,
                    sexo=user.sexo,
                    mappa_auth=user.mappa_auth,
                    mappa_valid_until=user.mappa_valid_until
                ),
                message="Authorized",
                validUntil=valid_until,
            )
        return AuthLoginResponse(message="Authorization not found or expired")
