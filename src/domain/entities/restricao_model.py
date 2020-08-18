from pydantic import BaseModel


class RestricaoModel(BaseModel):
    tipo: str
    nome: str
    descricao: str
