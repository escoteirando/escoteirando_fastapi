from pydantic import BaseModel
from typing import Optional, Union


class MappaUserRequest(BaseModel):
    user_id: int
    authentication: str
    user_name: Optional[Union[str, None]]
    auth_valid_until: Optional[int]

    sexo: Union[str, None]
    nascimento: Union[str, None]
    ueb_id: Optional[int]
