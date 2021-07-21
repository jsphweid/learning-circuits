from enum import Enum
from typing import Optional


class IdentifierType(Enum):
    STATIC = 0
    FIELD = 1
    ARG = 2
    VAR = 3


class SymbolTable:
    def __init__(self):
        pass

    def start_subroutine(self):
        # starts new subroutine scope (resets the subroutine's symbol table)
        pass

    def define(self, name: str, type: str, kind: IdentifierType) -> None:
        pass

    def var_count(self, kind: IdentifierType) -> int:
        pass

    def kind_of(self, name: str) -> Optional[IdentifierType]:
        pass

    def type_of(self, name: str) -> str:
        pass

    def index_of(self, name: str) -> int:
        pass
