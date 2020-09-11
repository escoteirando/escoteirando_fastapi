from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class MAPPAUserResponse(BaseModel):
    authorization: str
    auth_valid_until: int
    user_id: int
    nome_completo: str
    cod_grupo: int
    cod_regiao: str
    nom_grupo: str
    cod_modalidade: str
    sexo: Optional[str]
    nascimento: Optional[datetime]
