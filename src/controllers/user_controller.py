from fastapi import Response, status, Request
from fastapi.responses import JSONResponse
from typing import List
from src import app
from src.domain.responses.user_menu_response import UserMenuResponse


@app.get('/api/user/menu', response_model=List[UserMenuResponse])
async def get_menus(request: Request):
    user = app.USER
    return app.USER.get_user_menus(user)
