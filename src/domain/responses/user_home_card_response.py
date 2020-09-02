from typing import Optional

from pydantic import BaseModel


class UserHomeCardResponse(BaseModel):
    title: str
    route: str
    subtitle: Optional[str]
    image: Optional[str]
    flex: int = 4
