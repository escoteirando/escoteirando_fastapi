from enum import Enum


class AuthMessage(str, Enum):
    LOGIN_OK = "auth_login_ok"
    LOGOUT = "auth_logout"
    SUBSCRIBE_OK = "auth_subscribe_ok"
