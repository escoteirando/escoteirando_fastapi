from typing import List

from pydantic import BaseModel

from src.domain.entities.progressao_model import ProgressaoModel
from src.domain.entities.restricao_model import RestricaoModel
from src.domain.enums.area_desenvolvimento_enum import AreaDesenvolvimento


class AtividadeModel(BaseModel):
    area_desenv: AreaDesenvolvimento
    id_tipo: str
    duracao_min: int
    duracao_max: int
    nome: str
    descricao: str
    como_avaliar: str
    restricoes: List[RestricaoModel]
    progressoes: List[ProgressaoModel]
