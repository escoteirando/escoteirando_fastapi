from datetime import datetime

from pydantic import BaseModel


class MAPPAAssociadoResponse(BaseModel):
    codigo: int
    nome: str
    dataNascimento: datetime
    sexo: str
