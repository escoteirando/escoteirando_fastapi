from pydantic import BaseModel


class MAPPASecaoResponse(BaseModel):
    codigo: int
    nome: str
    tipoSecao: str
    codigoGrupo: int
    codigoRegiao: str
