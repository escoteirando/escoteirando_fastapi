from pydantic import BaseModel


class UserDataResponse(BaseModel):
    id: int
    name: str
    email: str
    full_name: str
    ueb_id: int
    mappa_user: str

    # nome_usuario: null,
    # nome_completo: null,
    # email: null,
    # nascimento: null,
    # sexo: null,
    # nivel: null,
    # nome_grupo: null,
    # cod_grupo: null,
    # cod_regiao: null,
    # tipo_sessao: null,
    # nome_sessao: null
