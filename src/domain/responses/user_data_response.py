from pydantic import BaseModel


class UserDataResponse(BaseModel):
    name: str
    email: str
    ueb_id: int
    mappa_user: str
