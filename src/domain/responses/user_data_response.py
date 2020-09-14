from datetime import date
from typing import Union

from pydantic import BaseModel


class UserDataResponse(BaseModel):
    id: int
    name: str
    email: str
    full_name: Union[str, None]
    ueb_id: int
    mappa_user: Union[str, None]
    mappa_auth: Union[str, None]
    mappa_valid_until: Union[int, None]
    nascimento: Union[date, None]
    sexo: Union[str, None]

    # nome_usuario: null,
    # nome_completo: null,
    # nivel: null,
    # nome_grupo: null,
    # cod_grupo: null,
    # cod_regiao: null,
    # tipo_sessao: null,
    # nome_sessao: null
