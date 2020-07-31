from pydantic import BaseModel
from typing import Optional


class AuthLoginResponse(BaseModel):
    authorization: Optional[str]
    validUntil: Optional[int]
    message: Optional[str]
