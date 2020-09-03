from src.domain.entities.atividade_model import AtividadeModel

from .base_repository import BaseRepository


class AtividadeRepository(BaseRepository):
    def __init__(self, connection):
        super().__init__(
            connection, collection_name="atividade", entity_type=AtividadeModel
        )
