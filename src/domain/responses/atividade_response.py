from datetime import datetime
from typing import List

from pydantic import BaseModel

from src.domain.entities.progressao_model import ProgressaoModel
from src.domain.entities.restricao_model import RestricaoModel
from src.domain.enums import AreaDesenvolvimento, TipoAtividade, TipoRamo

from .user_data_response import UserDataResponse


class AtividadeResponse(BaseModel):
    id: int
    area_desenv: AreaDesenvolvimento
    id_tipo: TipoAtividade
    ramo: TipoRamo
    duracao_min: int
    duracao_max: int
    nome: str
    descricao: str
    como_avaliar: str
    chaves: List[str]
    restricoes: List[RestricaoModel]
    progressoes: List[ProgressaoModel]
    data_criacao: datetime = datetime.now()
    usuario_criador: UserDataResponse
