from typing import List

import mappa
from src.domain.entities.user import User
from src.domain.responses.mappa import (MAPPASecaoResponse,
                                        MAPPASubsecaoResponse,
                                        MAPPAUserResponse)


class MAPPA_Service:

    def __init__(self, cache, user_service):
        self._cache = cache
        self._user_service = user_service

    def _mappa(self) -> mappa.MAPPAService:
        return mappa.MAPPAService(self._cache)

    def login(self, user: User, username: str, password: str):
        mappa = self._mappa()
        if mappa.login(username, password):
            user.mappa_user = username
            user.mappa_auth = mappa.authorization
            user.mappa_valid_until = mappa.auth_valid_until
            user.ueb_id = mappa.user_id

            user_info = mappa.get_user_info(mappa.user_id)

            user.full_name = user.full_name or user_info.get(
                'nome_completo', '')
            user.sexo = user.sexo or user_info.get('sexo', 'O')
            self._user_service.save_user(user)
            return True

    def get_secoes(self, user: User) -> List[MAPPASecaoResponse]:
        mappa = self._mappa()
        mappa.set_authorization(
            user.ueb_id, user.mappa_auth, user.mappa_valid_until)
        secoes = mappa.get_secoes(user.ueb_id)
        return [
            MAPPASecaoResponse(
                codigo=secao.codigo,
                nome=secao.nome,
                tipoSecao={1: 'A', 2: 'T', 3: 'S', 4: 'C'}.get(
                    secao.codigoTipoSecao, 'X'),
                codigoGrupo=secao.codigoGrupo,
                codigoRegiao=secao.codigoRegiao)
            for secao in secoes]

    def get_user_info(self, user_id, authorization, auth_valid_until):
        mappa = self._mappa()
        mappa.set_authorization(user_id, authorization, auth_valid_until)
        user_info = mappa.get_user_info(user_id, True)

        response = MAPPAUserResponse(
            authorization=user_info['autorizacao'],
            auth_valid_until=user_info['autorizacao_validade'],
            user_id=user_id,
            nome_completo=user_info['nome_completo'],
            cod_grupo=user_info['cod_grupo'],
            cod_regiao=user_info['cod_regiao'],
            nom_grupo=user_info['nom_grupo'],
            cod_modalidade=user_info['cod_modalidade'],
            sexo=user_info['sexo'],
            nascimento=user_info['data_nascimento'])

        return response

    def get_equipe(self, user: User, codigo_secao: int):
        mappa = self._mappa()
        mappa.set_authorization(
            user.ueb_id, user.mappa_auth, user.mappa_valid_until)
        mappa.get_equipe(user_id, cod_secao)
