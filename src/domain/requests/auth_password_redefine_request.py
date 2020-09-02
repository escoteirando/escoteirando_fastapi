from pydantic import BaseModel


class AuthPasswordRedefineRequest(BaseModel):

    authorization: str
    password: str
    email: str
