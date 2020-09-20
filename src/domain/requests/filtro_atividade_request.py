from typing import List, Optional

from pydantic import BaseModel

from src.domain.enums.area_desenvolvimento_enum import AreaDesenvolvimento
from src.domain.enums.tipo_atividade_enum import TipoAtividade
from src.domain.enums.tipo_ramo_enum import TipoRamo


class FiltroAtividadeRequest(BaseModel):
    area: Optional[AreaDesenvolvimento]
    atividade: Optional[TipoAtividade]
    ramo: Optional[TipoRamo]
    chaves: Optional[List[str]]
    limit: Optional[int]
    skip: Optional[int]
