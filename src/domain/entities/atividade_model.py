from typing import List

from pydantic import BaseModel

from src.domain.entities.progressao_model import ProgressaoModel
from src.domain.entities.restricao_model import RestricaoModel
from src.domain.enums import AreaDesenvolvimento, TipoAtividade
from datetime import datetime


class AtividadeModel(BaseModel):
    id: int
    area_desenv: AreaDesenvolvimento
    id_tipo: TipoAtividade
    duracao_min: int
    duracao_max: int
    nome: str
    descricao: str
    como_avaliar: str
    restricoes: List[RestricaoModel]
    progressoes: List[ProgressaoModel]
    data_criacao: datetime = datetime.now()
