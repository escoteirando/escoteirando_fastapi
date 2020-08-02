from pydantic import BaseModel
from typing import Optional


class AuthSubscribeResponse(BaseModel):
    success: bool
    message: Optional[str]
