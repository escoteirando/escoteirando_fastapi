from src.domain.responses.user_data_response import UserDataResponse
from typing import Optional

from pydantic import BaseModel


class AuthLoginResponse(BaseModel):
    authorization: Optional[str]
    validUntil: Optional[int]
    message: Optional[str]
    user: Optional[UserDataResponse]
