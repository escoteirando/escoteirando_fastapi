from enum import Enum


class AreaDesenvolvimento(str, Enum):
    fisico = 'f'
    intelectual = 'i'
    carater = 'c'
    afetivo = 'a'
    social = 's'
    espiritual = 'e'

    @classmethod
    def descricao(cls, area):
        area = str(area).lower()
        return {
            'f': 'Físico',
            'i': 'Intelectual',
            'c': 'Caráter',
            'a': 'Afetivo',
            's': 'Social',
            'e': 'Espiritual'
        }.get(area, 'Não identificado')
