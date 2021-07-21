from enum import Enum
from typing import NamedTuple


class IdentifierKind(Enum):
    STATIC = 0
    FIELD = 1
    ARG = 2
    VAR = 3


class _Info(NamedTuple):
    name: str
    type: str
    kind: IdentifierKind
    index: int


class SymbolTable:
    _class_scope: dict
    _fn_scope: dict

    def __init__(self):
        self._class_scope = SymbolTable._reset_dict()
        self._fn_scope = SymbolTable._reset_dict()

    @staticmethod
    def _reset_dict():
        return {
            IdentifierKind.STATIC: 0,
            IdentifierKind.FIELD: 0,
            IdentifierKind.ARG: 0,
            IdentifierKind.VAR: 0,
        }

    def __repr__(self):
        return f"SYMBOL TABLE\n" \
               f"class - {self._class_scope}\n" \
               f"fn - {self._fn_scope}\n"

    def start_subroutine(self) -> None:
        self._fn_scope = SymbolTable._reset_dict()

    def define(self, name: str, type: str, kind: IdentifierKind) -> None:
        # TODO: should throw error if already defined?
        if kind in {IdentifierKind.FIELD, IdentifierKind.STATIC}:
            reserved_index = self._class_scope[kind]
            self._class_scope[kind] += 1
            self._class_scope[name] = _Info(name, type, kind, reserved_index)
        else:
            reserved_index = self._fn_scope[kind]
            self._fn_scope[kind] += 1
            self._fn_scope[name] = _Info(name, type, kind, reserved_index)

    def var_count(self, kind: IdentifierKind) -> int:
        d = self._class_scope if kind in {IdentifierKind.FIELD, IdentifierKind.STATIC} else self._fn_scope
        return d[kind]

    def kind_of(self, name: str) -> IdentifierKind:
        return self._require_item_in_scope(name).kind

    def type_of(self, name: str) -> str:
        return self._require_item_in_scope(name).type

    def index_of(self, name: str) -> int:
        return self._require_item_in_scope(name).index

    def _require_item_in_scope(self, name: str) -> _Info:
        item = self._class_scope.get(name) or self._fn_scope.get(name)
        assert item, f"Item {name} was not in any scope..."
        return item
