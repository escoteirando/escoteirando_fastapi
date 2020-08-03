from typing import Optional

from pydantic import BaseModel


class AuthSubscribeResponse(BaseModel):
    success: bool
    message: Optional[str]
