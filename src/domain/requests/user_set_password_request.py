from pydantic import BaseModel


class UserSetPasswordRequest(BaseModel):
    email: str
    password: str
