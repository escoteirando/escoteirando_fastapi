from typing import List

from pydantic import BaseModel

from .mappa_associado_response import MAPPAAssociadoResponse


class MAPPASubsecaoResponse(BaseModel):
    codigo: int
    nome: str
    codigoSecao: int
    codigoLider: int
    codigoViceLider: int
    associados: List[MAPPAAssociadoResponse]
