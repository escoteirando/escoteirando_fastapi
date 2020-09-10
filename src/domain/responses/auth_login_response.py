from typing import Optional

from pydantic import BaseModel

from src.domain.responses.user_data_response import UserDataResponse


class AuthLoginResponse(BaseModel):
    authorization: Optional[str]
    validUntil: Optional[int]
    message: Optional[str]
    user: Optional[UserDataResponse]
