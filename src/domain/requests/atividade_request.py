from typing import List, Optional

from pydantic import BaseModel

# from src.domain.entities.restricao_model import RestricaoModel
from src.domain.enums import AreaDesenvolvimento, TipoAtividade, TipoRamo


class AtividadeRequest(BaseModel):
    id: int
    area_desenv: AreaDesenvolvimento
    id_tipo: TipoAtividade
    duracao_min: int
    duracao_max: int
    nome: str
    descricao: str
    como_avaliar: str
    # restricoes: Optional[List[RestricaoModel]]
    codigo_progressoes: Optional[List[int]]
    chaves: Optional[List[str]]
    ramo: TipoRamo
