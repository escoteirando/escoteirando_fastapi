from pydantic import BaseModel


class User(BaseModel):
    id: int
    name: str
    email: str
    ueb_id: int
    active: bool
    password_hash: str
