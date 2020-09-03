from typing import List

from fastapi import Request, Response

from src import app
from src.domain.requests import UserSetPasswordRequest
from src.domain.responses import BaseResponse, UserHomeCardResponse, UserMenuResponse


@app.get("/api/user/menu", response_model=List[UserMenuResponse])
async def get_menus(request: Request):
    user = request.scope["USER"]
    return app.USER.get_user_menu(user)


@app.post(
    "/api/user/password",
    response_model=BaseResponse,
    responses={200: {"model": BaseResponse}, 400: {"model": BaseResponse}},
)
async def set_password(
    password_request: UserSetPasswordRequest, request: Request, response: Response
):
    user = request.scope["USER"]
    success, msg = app.USER.set_password(user, password_request)
    if not success:
        response.status_code = 400

    return BaseResponse(ok=success, msg=msg)


@app.get("/api/user/home", response_model=List[UserHomeCardResponse])
async def get_user_home_cards(request: Request):
    user = request.scope["USER"]
    return app.USER.get_user_home_cards(user)
