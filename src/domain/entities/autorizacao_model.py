from datetime import datetime

from pydantic import BaseModel

from ..enums import TipoAutorizacao


class AutorizacaoModel(BaseModel):
    tipo: TipoAutorizacao = TipoAutorizacao.RedefinirSenha
    chave: str
    usuario: str
    valido_ate: datetime
