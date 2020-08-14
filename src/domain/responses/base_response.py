from typing import Optional, Union

from pydantic import BaseModel

from ..enums import AuthMessage, UserMessage


class BaseResponse(BaseModel):
    """ ok:bool, code, msg """
    ok: bool
    code: Union[AuthMessage, UserMessage]
    msg: Optional[str]
