from src.domain.responses.auth_subscribe_response import AuthSubscribeResponse
from fastapi import Response, status
from fastapi.responses import JSONResponse

from src import app
from src.app import get_logger
from src.domain.requests import AuthLoginRequest, AuthSubscribeRequest
from src.domain.responses import AuthLoginResponse

logger = get_logger(__name__)


@app.post("/auth/login", response_model=AuthLoginResponse)
async def login(request: AuthLoginRequest, response: Response):
    auth_response: AuthLoginResponse = app.AUTH.login(
        request.username, request.password)
    if auth_response.authorization:
        response.status_code = status.HTTP_200_OK
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED

    logger.info("Login: %s:***", request.username)
    return AuthLoginResponse(authorization=auth_response.authorization,
                             validUntil=auth_response.validUntil,
                             message=auth_response.message,
                             user=auth_response.user)


@app.post("/auth/logout", status_code=status.HTTP_202_ACCEPTED)
async def logout(authorization: str):
    logger.info("Logout: %s", authorization)
    return JSONResponse(
        status_code=status.HTTP_202_ACCEPTED,
        content={"msg": "Logged-out"}
    )


@app.post("/auth/user/{authorization}",
          status_code=status.HTTP_202_ACCEPTED,
          response_model=AuthLoginResponse)
async def get_authorization_data(authorization: str, response: Response):
    auth_response: AuthLoginResponse = app.AUTH.get_authorization_data(
        authorization)
    if auth_response.authorization:
        response.status_code = status.HTTP_200_OK
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED

    logger.info("Get Authorization data: %s", authorization)
    return auth_response


@app.post("/auth/subscribe",
          status_code=status.HTTP_202_ACCEPTED,
          response_model=AuthSubscribeResponse)
async def subscribe(request: AuthSubscribeRequest):
    logger.info("Subscribe: %s", request)
    return app.USER.create_user(request)
