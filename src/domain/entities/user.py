from datetime import date, datetime
from typing import Union

from pydantic import BaseModel, validator

from ..enums import UserLevel, TipoSexo, TipoRamo


class User(BaseModel):
    id: int
    name: str
    email: str
    full_name: Union[str, None]
    ueb_id: Union[int, None]  # user_id: int
    mappa_user: Union[str, None]  # user_name
    mappa_auth: Union[str, None]  # authentication
    mappa_valid_until: Union[int, None]  # auth_valid_until: Optional[int]
    sexo: Union[TipoSexo, None]
    nascimento: Union[datetime, None]
    ramo: Union[TipoRamo, None]
    active: bool
    password_hash: str
    creation_date: datetime
    validated: bool
    level: UserLevel = UserLevel.normal

    @validator("nascimento", pre=True)
    def convert_nascimento(cls, v):
        if isinstance(v, date) or isinstance(v.datetime):
            return datetime(v.year, v.month, v.day)
        return v
