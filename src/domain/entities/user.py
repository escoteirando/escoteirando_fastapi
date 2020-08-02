from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
    id: int
    name: str
    email: str
    ueb_id: Optional[int]
    active: bool
    password_hash: str
