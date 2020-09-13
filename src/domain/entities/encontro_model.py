from datetime import datetime
from typing import List

from pydantic import BaseModel

from src.domain.entities.atividade_model import AtividadeModel
from src.domain.enums import TipoRamo


class EncontroModel(BaseModel):
    id: int
    ramo: TipoRamo
    id_criador: int
    data_criacao: datetime
    duracao: int
    atividades: List[AtividadeModel]
