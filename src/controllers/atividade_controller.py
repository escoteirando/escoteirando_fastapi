from fastapi import Response

from src import app
from src.domain.entities.atividade_model import AtividadeModel


@app.get("/api/atividade/{id_atividade}", response_model=AtividadeModel)
def get_atividade(id_atividade: int, response: Response):
    pass
