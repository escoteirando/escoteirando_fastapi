from typing import Optional

from pydantic import BaseModel


class AuthLoginResponse(BaseModel):
    authorization: Optional[str]
    validUntil: Optional[int]
    message: Optional[str]
