from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    id: int
    name: str
    email: str
    ueb_id: Optional[int]
    mappa_user: Optional[str]
    active: bool
    password_hash: str
    creation_date: datetime
    validated: bool
