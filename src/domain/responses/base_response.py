from typing import Optional, Union

from pydantic import BaseModel


class BaseResponse(BaseModel):
    """ ok:bool, code, msg """
    ok: bool
    data: Optional[Union[dict, str]]
    msg: Optional[str]
