from datetime import datetime

from ..domain.entities.autorizacao_model import AutorizacaoModel
from .base_repository import BaseRepository


class ChaveAutorizacaoRepositorio(BaseRepository):
    def __init__(self, connection):
        super().__init__(
            connection, collection_name="autorizacao", entity_type=AutorizacaoModel
        )
        self._collection.create_index([("chave", 1)])

    def get_autorizacao(self, chave) -> AutorizacaoModel:
        auth = self._collection.find_one({"chave": chave})
        if auth:
            if auth.valido_ate > datetime.now():
                auth.update({"id": auth["_id"]})
                return AutorizacaoModel(**auth)
            else:
                self._collection.delete_one({"chave": chave})
