from src import app
from src.app.logger import get_logger
from src.domain.enums import AreaDesenvolvimento, TipoAtividade
from src.middleware.authorization_middleware import noauth_route

logger = get_logger(__name__)

noauth_route('/api/consts')


@app.get('/api/consts')
def get_all_consts():
    area_desenv = {x._value_: AreaDesenvolvimento.descricao(x._value_)
                   for x in AreaDesenvolvimento}
    tipo_atividade = {x._value_: TipoAtividade.descricao(x._value_)
                      for x in TipoAtividade}
    consts = {
        'area_desenv': area_desenv,
        'tipo_atv': tipo_atividade
    }

    logger.debug('CONSTS: %s', consts)
    return consts
