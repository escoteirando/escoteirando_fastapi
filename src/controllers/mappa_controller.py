import datetime
from typing import List, Optional

import dateutil.parser
from fastapi import Header, Request, Response, status

from mappa.models.internal.user_info import UserInfoModel
from src import app
from src.domain.entities.user import User
from src.domain.requests import AuthLoginRequest, MappaUserRequest
from src.domain.responses import (BaseResponse, MAPPASecaoResponse,
                                  MAPPAUserResponse)


@app.post('/api/mappa/login', response_model=MAPPAUserResponse)
def login(auth: AuthLoginRequest, response: Response):
    if not app.MAPPA.login(auth.username, auth.password):
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return BaseResponse(ok=False)

    user_info: UserInfoModel = app.MAPPA.get_user_info(app.MAPPA.user_id) or {}

    response_data = MAPPAUserResponse(
        authorization=app.MAPPA.authorization,
        auth_valid_until=app.MAPPA.auth_valid_until,
        user_id=app.MAPPA.user_id,
        nome_completo=user_info.nome_completo,
        cod_grupo=user_info.cod_grupo,
        cod_regiao=user_info.cod_regiao,
        nom_grupo=user_info.nom_grupo,
        cod_modalidade=user_info.cod_modalidade,
        sexo=user_info.sexo,
        data_nascimento=user_info.data_nascimento
    )

    return response_data


@app.post('/api/mappa/auth', response_model=MAPPAUserResponse)
def auth(user_id: int, authorization: str,
         auth_valid_until: int, response: Response):
    app.MAPPA.set_authorization(user_id, authorization, auth_valid_until)


@app.post('/api/mappa/secoes', response_model=List[MAPPASecaoResponse])
def user_info(user_request: MappaUserRequest, response: Response):
    if app.MAPPA.is_authorized(user_request.user_id):
        pass
    elif user_request.user_name:
        if not app.MAPPA.reload_authorization(user_request.user_name):
            response.status_code = status.HTTP_401_UNAUTHORIZED
            return
    elif user_request.authentication and user_request.auth_valid_until:
        app.MAPPA.set_authorization(
            user_request.user_id,
            user_request.authentication, user_request.auth_valid_until)
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return
    secoes = app.MAPPA.get_secoes(user_request.user_id)
    response = []
    for secao in secoes:
        response.append(
            MAPPASecaoResponse(
                codigo=secao.codigo,
                nome=secao.nome,
                tipo=secao.tipo_secao_str))
    return response


@app.post('/api/mappa/save')
def save_user(user_request: MappaUserRequest,
              request: Request,
              response: Response):
    user: User = request.scope['USER']
    if not user:
        response.status_code = status.HTTP_404_NOT_FOUND
        return
    try:
        user.ueb_id = user_request.ueb_id
        user.mappa_auth = user_request.authentication
        user.mappa_valid_until = user_request.auth_valid_until
        user.sexo = user_request.sexo
        try:
            user.data_nascimento = dateutil.parser.parse(
                user_request.data_nascimento)
        except:
            user.data_nascimento = None
        if app.USER.save_user(user):
            response.status_code = status.HTTP_202_ACCEPTED
        else:
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    except Exception as exc:

        pass
