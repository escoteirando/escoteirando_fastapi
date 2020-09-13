from pydantic import BaseModel
from datetime import datetime


class AgendaEncontro(BaseModel):
    id: int
    id_encontro: int
    data_inicio: datetime
    codigo_grupo: int
    codigo_regiao: str
    id_usuario: int
