from pydantic import BaseModel


class AuthSubscribeRequest(BaseModel):
    username: str
    ueb_id: int
    password: str
    email: str
