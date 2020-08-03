from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    id: int
    name: str
    email: str
    ueb_id: Optional[int]
    active: bool
    password_hash: str
    creation_date: datetime
    validated: bool
