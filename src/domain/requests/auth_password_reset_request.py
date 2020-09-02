from pydantic import BaseModel


class AuthPasswordResetRequest(BaseModel):
    email: str
