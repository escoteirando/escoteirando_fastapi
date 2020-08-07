from src.domain.responses.user_data_response import UserDataResponse
import time
import uuid

from src.app import get_logger
from src.domain.entities.user import User
from src.domain.responses import AuthLoginResponse

logger = get_logger(__name__)


class AuthorizationService:

    def __init__(self, cache_service, user_service, config):
        logger.info('INIT')
        self._cache = cache_service
        self._user_service = user_service
        self._config = config

    def _auth_key(self, key: str) -> str:
        return f"auth_{key}"

    def create_authorizaton(self, user: User) -> str:
        new_auth = str(uuid.uuid1())
        if self._cache.set_value(self._auth_key(new_auth),
                                 user.dict(),
                                 self._config.AUTHORIZATION_TTL):
            return new_auth

    def user_from_authorization(self, authorization: str) -> User:
        obj = self._cache.get_value(self._auth_key(authorization))
        if obj:
            obj = User.construct(**obj)
        return obj

    def login(self, username: str, password: str) -> AuthLoginResponse:
        user: User = self._user_service.get_user(username)
        if not user:
            return AuthLoginResponse(message='User not found')

        if not self._user_service.is_valid_password(user, password):
            return AuthLoginResponse(message='Invalid password')

        if not user.active:
            return AuthLoginResponse(message="User is inactive")

        valid_until = time.time()+self._config.AUTHORIZATION_TTL
        auth = self.create_authorizaton(user)
        if not auth:
            return AuthLoginResponse(authorization=None,
                                     message="Authorization engine failed",
                                     valid_until=0)
        return AuthLoginResponse(authorization=auth,
                                 message="Authorized",
                                 validUntil=valid_until,
                                 user=UserDataResponse(name=user.name,
                                                       email=user.email))

    def get_authorization_data(self, authorization: str) -> AuthLoginResponse:
        user = self.user_from_authorization(authorization)
        if user:
            return AuthLoginResponse(authorization=authorization,
                                     user=UserDataResponse(name=user.name,
                                                           email=user.email),
                                     message="Authorized")
        return AuthLoginResponse(message='Authorization not found or expired')
