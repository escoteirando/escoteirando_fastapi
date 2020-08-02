from fastapi import status, Response
from fastapi.responses import JSONResponse
from src import app
from src.domain.requests import AuthLoginRequest, AuthSubscribeRequest
from src.domain.responses import AuthLoginResponse
import logging


logger = logging.getLogger(__name__)


@app.post("/auth/login", response_model=AuthLoginResponse)
async def login(request: AuthLoginRequest):
    auth_response = app.AUTH.login(request.username, request.password)
    logger.info("Login: %s:***", request.username)
    return AuthLoginResponse(authorization='abcd')


@app.post("/auth/logout", status_code=status.HTTP_202_ACCEPTED)
async def logout(authorization: str):
    logger.info("Logout: %s", authorization)
    return JSONResponse(
        status_code=status.HTTP_202_ACCEPTED,
        content={"msg": "Logged-out"}
    )


@app.post("/auth/subscribe", status_code=status.HTTP_202_ACCEPTED)
async def subscribe(request: AuthSubscribeRequest):
    logger.info("Subscribe: %s", request)
    app.USER.create_user(request)
