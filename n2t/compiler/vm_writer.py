from enum import Enum
from typing import List


class Segment(Enum):
    CONST = "const"
    ARG = "argument"
    LOCAL = "local"
    STATIC = "static"
    POINTER = "pointer"
    THIS = "this"
    THAT = "that"
    TEMP = "temp"


class Command(Enum):
    ADD = "add"
    SUB = "sub"
    NEG = "neg"
    EQ = "eq"
    GT = "gt"
    LT = "lt"
    AND = "and"
    OR = "or"
    NOT = "not"


class VMWriter:
    _vm_lines: List[str]

    def __init__(self):
        self._vm_lines = []

    def write_push(self, segment: Segment, index: int) -> None:
        self._vm_lines.append(f"push {segment.value} {index}")

    def write_pop(self, segment: Segment, index: int) -> None:
        self._vm_lines.append(f"pop {segment.value} {index}")

    def write_arithmetic(self, command: Command) -> None:
        self._vm_lines.append(command.value)

    def write_label(self, label: str) -> None:
        self._vm_lines.append(f"label {label}")

    def write_goto(self, label: str) -> None:
        self._vm_lines.append(f"goto {label}")

    def write_if(self, label: str) -> None:
        self._vm_lines.append(f"if-goto {label}")

    def write_call(self, name: str, num_args: int) -> None:
        self._vm_lines.append(f"call {name} {num_args}")

    def write_fn(self, label: str, num_locals: int) -> None:
        self._vm_lines.append(f"function {label} {num_locals}")

    def write_return(self) -> None:
        self._vm_lines.append("return")

    def get_lines(self) -> List[str]:
        return self._vm_lines
