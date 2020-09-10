from pydantic import BaseModel


class AuthSubscribeRequest(BaseModel):
    username: str
    password: str
    email: str
