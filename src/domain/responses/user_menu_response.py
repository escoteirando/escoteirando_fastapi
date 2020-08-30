from pydantic import BaseModel
from typing import Optional


class UserMenuResponse(BaseModel):
    id: int
    text: str
    route: str
    icon: Optional[str]
