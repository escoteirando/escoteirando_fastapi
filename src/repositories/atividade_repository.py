from typing import List

from src.domain.entities.atividade_model import AtividadeModel

from .base_repository import BaseRepository


class AtividadeRepository(BaseRepository):
    def __init__(self, connection):
        super().__init__(
            connection, collection_name="atividade", entity_type=AtividadeModel
        )

    def find(self, filter, skip: int = 0, limit: int = 0) \
            -> List[AtividadeModel]:
        atividades = self._collection.find(filter)
        return [AtividadeModel({**model, "id": model["_id"]})
                for model in atividades]
