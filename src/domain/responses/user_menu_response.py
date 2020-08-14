from pydantic import BaseModel


class UserMenuResponse(BaseModel):
    id: int
    text: str
    route: str
    icon: str
