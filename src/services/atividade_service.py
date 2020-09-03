from src.app import get_logger
from src.repositories.atividade_repository import AtividadeRepository

logger = get_logger(__name__)


class AtividadeService:
    def __init__(self, repository: AtividadeRepository):
        self._repository: AtividadeRepository = repository
