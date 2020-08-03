from typing import Optional

from fastapi import Response, status
from pydantic import BaseModel

from src.app import app
from src.domain.requests.auth_subscribe_request import AuthSubscribeRequest
from src.domain.responses.auth_subscribe_response import AuthSubscribeResponse


class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None


@app.get("/api/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


@app.put("/api/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}


@app.get("/test/email")
def send_email():
    mailer = app.MAILER
    if not mailer.is_valid_email('guionardo@gmail.com'):
        print("Email inválido")
    mailer.send('guionardo@gmail.com',
                'Teste de envio', 'Corpo do e-mail\nNova linha')


@app.get("/test/user/{username}")
def get_user(username):
    user = app.USER.get_user_by_name(username)
    return user


@app.get("/test/user_email/{email}")
def get_user_email(email):
    user = app.USER.get_user_by_email(email)
    return user


@app.post("/test/usuario", response_model=AuthSubscribeResponse)
def create_user(user: AuthSubscribeRequest, response: Response):
    create_response = app.USER.create_user(user)
    if not create_response.success:
        response.status_code = status.HTTP_400_BAD_REQUEST
    return create_response
