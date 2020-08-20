from fastapi import Response, status

from src import app
from src.domain.responses import BaseResponse, MAPPAUserResponse
from src.middleware.authorization_middleware import noauth_route
from mappa.models.internal.user_info import UserInfoModel

noauth_route('/api/mappa/login')


@app.post('/api/mappa/login', response_model=MAPPAUserResponse)
def login(username: str, password: str, response: Response):
    if not app.MAPPA.login(username, password):
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
        cod_modalidade=user_info.cod_modalidade
    )

    return response_data


@app.post('/api/mappa/auth', response_model=MAPPAUserResponse)
def auth(user_id: int, authorization: str, auth_valid_until: int, response: Response):
    app.MAPPA.set_authorization(user_id, authorization, auth_valid_until)
