from datetime import datetime, timedelta
from typing import List

from mappa_api.models import Login, Secao, Progressao
from mappa_api.models.enums import Ramo
from mappa_api.services import (BIService, EscotistaService, KBService,
                                MAPPAService)
from src.domain.entities.user import User
from src.domain.responses.mappa import (MAPPAProgressaoResponse,
                                        MAPPASecaoResponse, MAPPAUserResponse)


class MAPPA_Service:

    def __init__(self, cache, user_service, progressao_repository):
        self._cache = cache
        self._user_service = user_service
        self._progressao_repository = progressao_repository

    def _mappa(self) -> MAPPAService:
        return MAPPAService(self._cache)

    def get_login(self, user: User) -> Login:
        if not user or \
                user.mappa_valid_until < datetime.now().timestamp():
            return None
        created = datetime.fromtimestamp(
            user.mappa_valid_until - 86400).strftime('%Y-%m-%dT%H:%M:%S')
        login = Login(id=user.mappa_auth,
                      ttl=86400,
                      created=created,
                      userId=user.ueb_id)
        if login.is_valid:
            return login

    def login(self, user: User, username: str, password: str):
        mappa = self._mappa()

        login = self.get_login(user)
        if login:
            return True

        login = mappa.login(username, password)
        if not login:
            return False

        user.mappa_user = username
        user.mappa_auth = login.id
        user.mappa_valid_until = int((
            login.created+timedelta(seconds=login.ttl)).timestamp())
        user.ueb_id = login.userId
        escotista_service = EscotistaService(mappa)
        escotista = escotista_service.get_escotista(login)
        associado = escotista_service.get_associado(
            login, escotista.codigoAssociado)

        user.sexo = associado.sexo
        user.full_name = escotista.nomeCompleto
        self._user_service.save_user(user)
        return True

    def get_secoes(self, user: User) -> List[Secao]:
        login = self.get_login(user)
        if not login:
            return None

        mappa = self._mappa()
        escotista_service = EscotistaService(mappa)
        secoes = escotista_service.get_secoes(login)
        return secoes

        mappa.set_authorization(
            user.ueb_id, user.mappa_auth, user.mappa_valid_until)
        secoes = mappa.get_secoes(user.ueb_id)
        return [
            MAPPASecaoResponse(
                codigo=secao.codigo,
                nome=secao.nome,
                tipoSecao={1: 'A', 2: 'E', 3: 'S', 4: 'C'}.get(
                    secao.codigoTipoSecao, 'X'),
                codigoGrupo=secao.codigoGrupo,
                codigoRegiao=secao.codigoRegiao)
            for secao in secoes]

    def get_user_info(self, user: User):
        login = self.get_login(user)
        if not login:
            return None

        mappa = self._mappa()
        escotista_service = EscotistaService(mappa)
        escotista = escotista_service.get_escotista(login)
        grupo = escotista_service.get_grupo(
            login, escotista.codigoGrupo, escotista.codigoRegiao)
        associado = escotista_service.get_associado(
            login, escotista.codigoAssociado)

        response = MAPPAUserResponse(
            authorization=user.mappa_auth,
            auth_valid_until=user.mappa_valid_until,
            user_id=user.ueb_id,
            nome_completo=escotista.nomeCompleto,
            cod_grupo=escotista.codigoGrupo,
            cod_regiao=escotista.codigoRegiao,
            nom_grupo=grupo.nome,
            cod_modalidade=associado.codigoRamo,
            sexo=associado.sexo,
            nascimento=associado.dataNascimento)

        return response

    def get_equipe(self, user: User, codigo_secao: int):
        login = self.get_login(user)
        if not login:
            return None

        mappa = self._mappa()
        escotista_service = EscotistaService(mappa)
        equipe = escotista_service.get_equipe(login, codigo_secao)
        return equipe

    def progressao_mensal_secao(self, user: User, codigo_secao: int):
        login = self.get_login(user)
        if not login:
            return None
        bi = BIService(self._mappa())
        progressoes = bi.get_progressao_secao(login, codigo_secao)
        return progressoes

    def progressoes_ramo(self, user: User, codigo_ramo: str):
        ramo = Ramo(codigo_ramo)
        progressoes = self.get_progressoes_repo(ramo)
        if progressoes:
            return progressoes
        login = self.get_login(user)
        if not login:
            return None
        mappa = self._mappa()
        kb_service = KBService(mappa)
        progressoes = kb_service.get_progressoes(login, ramo)
        result = [MAPPAProgressaoResponse(
            codigo=x.codigo,
            descricao=x.descricao,
            codigoUeb=x.codigoUeb,
            ordenacao=x.ordenacao,
            areaDesenvolvimento=x.area_desenvolvimento())
            for x in progressoes]
        self.save_progressoes_repo(progressoes)
        return result

    def get_progressoes_repo(self, ramo: Ramo) -> List[Progressao]:
        """ Retorna todas as progressões disponíveis no banco de dados"""
        if ramo is Ramo.Alcateia:
            caminhos = [1, 2, 3]
        elif ramo is Ramo.TropaEscoteira:
            caminhos = [4, 5, 6]
        elif ramo is Ramo.TropaSenior:
            caminhos = [11, 12]
        elif ramo is Ramo.ClaPioneiro:
            caminhos = [15, 16]
        else:
            caminhos = [1, 2, 3, 4, 5, 6, 11, 12,
                        13, 14, 15, 16, 17, 18, 19, 20]
        filtro = {"codigoCaminho": {"$in": caminhos}}
        result = self._progressao_repository.find(filtro)
        return result

    def save_progressoes_repo(self, progressoes: List[Progressao]):
        for progressao in progressoes:
            self._progressao_repository.save(progressao)
