from datetime import datetime
from typing import List

from src.app import get_logger
from src.domain.entities.atividade_model import AtividadeModel
from src.domain.entities.user import User
from src.domain.requests import AtividadeRequest, FiltroAtividadeRequest
from src.repositories.atividade_repository import AtividadeRepository

logger = get_logger(__name__)


class AtividadeService:
    def __init__(self, repository: AtividadeRepository):
        self._repository: AtividadeRepository = repository

    def salvar_atividade(self, user: User, atividade: AtividadeRequest) \
            -> AtividadeModel:
        if atividade.id > 0:
            atv: AtividadeModel = self._repository.get_by_id(atividade.id)
            atv.area_desenv = atividade.area_desenv
            atv.id_tipo = atividade.id_tipo
            atv.duracao_min = atividade.duracao_min
            atv.duracao_max = atividade.duracao_max
            atv.nome = atividade.nome
            atv.descricao = atividade.descricao
            atv.como_avaliar = atividade.como_avaliar
            atv.progressoes = []
            atv.ramo = atividade.ramo
            atv.chaves = atividade.chaves
        else:
            atv = AtividadeModel(
                area_desenv=atividade.area_desenv,
                id_tipo=atividade.id_tipo,
                duracao_min=atividade.duracao_min,
                duracao_max=atividade.duracao_max,
                nome=atividade.nome,
                descricao=atividade.descricao,
                como_avaliar=atividade.como_avaliar,
                progressoes=[],
                ramo=atividade.ramo,
                chaves=atividade.chaves,
                data_criacao=datetime.now(),
                usuario_criador=user)

        if self._repository.save(atv):
            return atv

    def obter_atividade(self, id: int) -> AtividadeModel:
        return self._repository.get_by_id(id)

    def filtro_atividade(self, filtro: FiltroAtividadeRequest) \
            -> List[AtividadeModel]:
        f = {}
        if filtro.area:
            f["area_desenv"] = filtro.area
        if filtro.atividade:
            f["id_tipo"] = filtro.atividade
        if filtro.ramo:
            f["ramo"] = filtro.ramo
        if filtro.chaves:
            f["chaves"] = {"$in": filtro.chaves}
        if not filtro.limit:
            filtro.limit = 0
        if not filtro.skip:
            filtro.skip = 0

        return self._repository.find(filtro, filtro.skip, filtro.limit)
