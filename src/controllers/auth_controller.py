from fastapi import Response, status

from src import app
from src.app import get_logger
from src.domain.enums import AuthMessage
from src.domain.requests import (
    AuthLoginRequest,
    AuthPasswordRedefineRequest,
    AuthPasswordResetRequest,
    AuthSubscribeRequest,
)
from src.domain.responses import AuthLoginResponse, BaseResponse

logger = get_logger(__name__)


@app.post("/auth/login", response_model=AuthLoginResponse)
async def login(request: AuthLoginRequest, response: Response):
    auth_response: AuthLoginResponse = app.AUTH.login(
        request.username, request.password
    )
    if auth_response.authorization:
        response.status_code = status.HTTP_200_OK
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED

    try:
        response = AuthLoginResponse(
            authorization=auth_response.authorization,
            validUntil=auth_response.validUntil,
            message=auth_response.message,
            user=auth_response.user,
        )

        logger.info("Login: %s:***", request.username)
        return response
    except Exception as exc:
        logger.exception("LOGIN: %s", exc)


@app.post(
    "/auth/logout", status_code=status.HTTP_202_ACCEPTED, response_model=BaseResponse
)
async def logout(authorization: str):
    logger.info("Logout: %s", authorization)
    app.AUTH.clear_authorizationi(authorization)
    return BaseResponse(ok=True, msg=AuthMessage.LOGOUT)


@app.post(
    "/auth/user/{authorization}",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=AuthLoginResponse,
)
async def get_authorization_data(authorization: str, response: Response):
    auth_response: AuthLoginResponse = app.AUTH.get_authorization_data(authorization)
    if auth_response.authorization:
        response.status_code = status.HTTP_200_OK
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED

    logger.info("Get Authorization data: %s", authorization)
    return auth_response

    try:
        response = AuthLoginResponse(
            authorization=auth_response.authorization,
            validUntil=auth_response.validUntil,
            message=auth_response.message,
            user=auth_response.user,
        )

        logger.info("Login: %s:***", response.user.name)
        return response
    except Exception as exc:
        logger.exception("LOGIN: %s", exc)


@app.post(
    "/auth/subscribe", status_code=status.HTTP_202_ACCEPTED, response_model=BaseResponse
)
async def subscribe(request: AuthSubscribeRequest):
    logger.info("Subscribe: %s", request)
    return app.USERS.create_user(request)


@app.post(
    "/auth/password/request",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=BaseResponse,
)
async def request_password_reset(password_reset: AuthPasswordResetRequest):
    logger.info("Password reset request: %s", password_reset.email)
    app.USER_PASS.send_password_reset_email(password_reset.email)
    return BaseResponse(ok=True)


@app.get(
    "/auth/password/{key}", status_code=status.HTTP_200_OK, response_model=BaseResponse
)
async def password_check_key(key: str, response: Response):
    logger.info("Password.Key %s", key)
    user = app.USER_PASS.validate_password_reset_key(key)
    if not user:
        response.status_code = status.HTTP_404_NOT_FOUND
    else:
        return BaseResponse(ok=True, data={"email": user.email})


@app.post(
    "/auth/password/reset",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=BaseResponse,
)
async def password_reset(
    password_reset: AuthPasswordRedefineRequest, response: Response
):
    logger.info("Password redefine request: %s", password_reset.authorization)
    success, msg = app.USER_PASS.redefine_password(password_reset)
    if success:
        response.status_code = status.HTTP_202_ACCEPTED
        return BaseResponse(ok=True, msg="Senha atualizada com sucesso")
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return BaseResponse(ok=False, msg=msg)
