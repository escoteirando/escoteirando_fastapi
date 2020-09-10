from typing import List

from fastapi import Request, Response, status

from src import app
from src.domain.requests import UserProfileRequest, UserSetPasswordRequest
from src.domain.responses import (BaseResponse, UserHomeCardResponse,
                                  UserMenuResponse)


@app.get("/api/user/menu", response_model=List[UserMenuResponse])
async def get_menus(request: Request):
    user = request.scope["USER"]
    return app.USERS.get_user_menu(user)


@app.post(
    "/api/user/password",
    response_model=BaseResponse,
    responses={200: {"model": BaseResponse}, 400: {"model": BaseResponse}},
)
async def set_password(password_request: UserSetPasswordRequest,
                       request: Request, response: Response):
    user = request.scope["USER"]
    success, msg = app.USER.set_password(user, password_request)
    if not success:
        response.status_code = 400

    return BaseResponse(ok=success, msg=msg)


@app.get("/api/user/home", response_model=List[UserHomeCardResponse])
async def get_user_home_cards(request: Request):
    user = request.scope["USER"]
    return app.USERS.get_user_home_cards(user)


@app.post('/api/user/profile', response_model=BaseResponse)
async def save_profile(profile: UserProfileRequest,
                       request: Request, response: Response):
    user = request.scope["USER"]
    motivo_falha = app.USERS.save_profile(user, profile)
    if motivo_falha:
        response.status_code = status.HTTP_406_NOT_ACCEPTABLE
        return BaseResponse(ok=False, msg=motivo_falha)
    else:
        return BaseResponse(ok=True)
