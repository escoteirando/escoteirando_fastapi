from pydantic import BaseModel
from src.domain.enums import TipoRestricao


class RestricaoModel(BaseModel):
    id: int
    tipo: TipoRestricao
    nome: str
    descricao: str
