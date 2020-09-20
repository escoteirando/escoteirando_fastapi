from pydantic import BaseModel


class MAPPAProgressaoResponse(BaseModel):
    codigo: int
    descricao: str
    codigoUeb: str
    ordenacao: int    
    areaDesenvolvimento: str
