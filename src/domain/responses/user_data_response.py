from pydantic import BaseModel


class UserDataResponse(BaseModel):
    name: str
    email: str
