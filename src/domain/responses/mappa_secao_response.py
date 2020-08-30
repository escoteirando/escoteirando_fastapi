from pydantic import BaseModel


class MAPPASecaoResponse(BaseModel):
    codigo: int
    nome: str    
    tipo: str
