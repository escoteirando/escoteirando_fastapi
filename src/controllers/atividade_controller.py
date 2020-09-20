from typing import List

from fastapi import Request, Response, status

from src import app
from src.domain.entities.atividade_model import AtividadeModel
from src.domain.entities.user import User
from src.domain.requests import AtividadeRequest, FiltroAtividadeRequest


@app.get("/api/atividade/{id}", response_model=AtividadeModel)
async def get_atividade(id: int, request: Request, response: Response):
    user: User = request.scope["USER"]
    if not user:
        response.status_code = status.HTTP_404_NOT_FOUND
        return
    result = app.ATV.obter_atividade(id)
    if not result:
        response.status_code = status.HTTP_404_NOT_FOUND
    else:
        return result


@app.post('/api/atividade', response_model=AtividadeModel)
async def post_atividade(atividade: AtividadeRequest,
                         request: Request, response: Response):
    user: User = request.scope["USER"]
    if not user:
        response.status_code = status.HTTP_404_NOT_FOUND
        return

    result = app.ATV.salvar_atividade(user, atividade)
    return result


@app.get('/api/atividade/:filtro', response_model=List[AtividadeModel])
async def get_atividades(filtro: FiltroAtividadeRequest,
                         request: Request, response: Response):
    result = app.ATV.filtro_atividade(filtro)
    return result
