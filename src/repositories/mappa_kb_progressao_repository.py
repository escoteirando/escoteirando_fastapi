from typing import List

from mappa_api.models.mappa.progressao import Progressao

from .base_repository import BaseRepository


class MAPPAKBProgressaoRepository(BaseRepository):

    def __init__(self, connection):
        super().__init__(connection,
                         collection_name="mappa_progressao",
                         entity_type=Progressao,
                         id_field="codigo")

    def find(self, filter) -> List[Progressao]:
        progressoes = self._collection.find(filter)
        return [Progressao(**{**model, **{"codigo": model["_id"]}})
                for model in progressoes]
