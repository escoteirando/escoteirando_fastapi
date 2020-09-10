from enum import Enum


class TipoSexo(str, Enum):
    Masculino = 'M'
    Feminino = 'F'
    Outros = 'O'
