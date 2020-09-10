from enum import Enum


class TipoRamo(str, Enum):
    Alcateia = "A"
    TropaEscoteira = "E"
    TropaSenior = "S"
    ClaPioneiro = "C"
