from enum import Enum


class TipoAtividade(str, Enum):
    cerimonia = "c"
    quebra_gelo = "q"
    cancao = "m"
    intervalo = "i"
    instrucao = "e"
    jogo = "j"
    historia = "h"

    @classmethod
    def descricao(cls, tipo):
        tipo = str(tipo).lower()
        return {
            "c": "Cerimônia",
            "q": "Quebra-gelo",
            "m": "Canção",
            "i": "Intervalo",
            "e": "Instrução",
            "j": "Jogo",
            "h": "História",
        }.get(tipo, "Não identificado")
