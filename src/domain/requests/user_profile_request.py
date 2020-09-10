from datetime import date

from pydantic import BaseModel

from src.domain.enums import TipoRamo, TipoSexo


class UserProfileRequest(BaseModel):
    name: str
    mappa_user: str
    email: str
    nascimento: date
    sexo: TipoSexo
    ramo: TipoRamo
