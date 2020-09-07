from typing import List

import dateutil.parser
from fastapi import Request, Response, status

from mappa.models.internal.user_info import UserInfoModel
from mappa_api.models import Secao
from src import app
from src.domain.entities.user import User
from src.domain.requests import AuthLoginRequest, MappaUserRequest
from src.domain.responses import BaseResponse
from src.domain.responses.mappa import (MAPPASecaoResponse,
                                        MAPPASubsecaoResponse,
                                        MAPPAUserResponse)


def verificar_usuario(request: Request, response: Response, testar_user_id: bool = True):
    user: User = request.scope["USER"]
    if not user:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return (None, BaseResponse(ok=False,
                                   msg="Usuário não está logado"))

    if testar_user_id and user.ueb_id < 1:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return (user, BaseResponse(ok=False,
                                   msg="Usuário não tem registro de identidade da UEB"))

    return user, None


@app.post("/api/mappa/login", response_model=MAPPAUserResponse)
async def mappa_login(auth: AuthLoginRequest, request: Request, response: Response):
    user, result = verificar_usuario(request, response, False)

    if not user:
        return result

    if not app.MAPPA.login(user, auth.username, auth.password):
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return BaseResponse(ok=False)

    user_info: UserInfoModel = app.MAPPA.get_user_info(
        user.ueb_id, user.mappa_auth, user.mappa_valid_until) or {}

    return user_info


@app.get('/api/mappa/user_info', response_model=MAPPAUserResponse)
async def mappa_get_user_info(request: Request, response: Response):
    user, result = verificar_usuario(request, response)
    if result:
        return result

    user_info: UserInfoModel = app.MAPPA.get_user_info(
        user.ueb_id, user.mappa_auth, user.mappa_valid_until)

    return user_info


@app.get('/api/mappa/secoes', response_model=List[Secao])
async def mappa_get_secoes(request: Request, response: Response):
    user, result = verificar_usuario(request, response)
    if result:
        return result
    return app.MAPPA.get_secoes(user)


@app.get('/api/mappa/equipe/{codigo_secao}', response_model=List[MAPPASubsecaoResponse])
async def mappa_get_equipe(request: Request, response: Response):
    user, result = verificar_usuario(request, response)
    if result:
        return result
    return app.MAPPA.get_equipe(user, request.path_params['codigo_secao'])


@ app.post("/api/mappa/auth", response_model=MAPPAUserResponse)
def auth(user_id: int, authorization: str, auth_valid_until: int, response: Response):
    app.MAPPA.set_authorization(user_id, authorization, auth_valid_until)


@ app.post("/api/mappa/secoes", response_model=List[MAPPASecaoResponse])
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
            user_request.authentication,
            user_request.auth_valid_until,
        )
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return
    secoes = app.MAPPA.get_secoes(user_request.user_id)
    response = []
    for secao in secoes:
        response.append(
            MAPPASecaoResponse(
                codigo=secao.codigo, nome=secao.nome, tipo=secao.tipo_secao_str
            )
        )
    return response


@ app.post("/api/mappa/save")
def save_user(user_request: MappaUserRequest, request: Request, response: Response):
    user: User = request.scope["USER"]
    if not user:
        response.status_code = status.HTTP_404_NOT_FOUND
        return
    try:
        user.ueb_id = user_request.ueb_id
        user.mappa_user = user_request.user_name
        user.mappa_auth = user_request.authentication
        user.mappa_valid_until = user_request.auth_valid_until
        user.sexo = user_request.sexo
        try:
            user.nascimento = dateutil.parser.parse(user_request.nascimento)
        except:
            user.nascimento = None
        if app.USERS.save_user(user):
            response.status_code = status.HTTP_202_ACCEPTED
        else:
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    except Exception as exc:

        pass
