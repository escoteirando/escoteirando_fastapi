from datetime import datetime
from typing import Union

from pydantic import BaseModel

from ..enums import UserLevel


class User(BaseModel):
    id: int
    name: str
    email: str
    ueb_id: Union[int, None]  # user_id: int
    mappa_user: Union[str, None]  # user_name
    mappa_auth: Union[str, None]  # authentication
    mappa_valid_until: Union[int, None]  # auth_valid_until: Optional[int]
    sexo: Union[str, None]
    data_nascimento: Union[datetime, None]

    active: bool
    password_hash: str
    creation_date: datetime
    validated: bool
    level: UserLevel = UserLevel.normal
