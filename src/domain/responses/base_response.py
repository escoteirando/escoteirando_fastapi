from typing import Optional

from pydantic import BaseModel


class BaseResponse(BaseModel):
    """ ok:bool, code, msg """
    ok: bool
    data: Optional[dict]
    msg: Optional[str]
