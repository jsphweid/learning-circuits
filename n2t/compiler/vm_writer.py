from enum import Enum


class Segment(Enum):
    CONST = 0
    ARG = 1
    LOCAL = 2
    STATIC = 3
    POINTER = 4
    THIS = 5
    THAT = 6
    TEMP = 7


class Command(Enum):
    ADD = 0
    SUB = 1
    NEG = 2
    EQ = 3
    GT = 4
    LT = 5
    AND = 6
    OR = 7
    NOT = 8


class VMWriter:
    def __init__(self):
        pass

    def write_push(self, segment: Segment, index: int) -> None:
        pass

    def write_pop(self, segment: Segment, index: int) -> None:
        pass

    def write_arithmetic(self, command: Command) -> None:
        pass

    def write_label(self, label: str) -> None:
        pass

    def write_goto(self, label: str) -> None:
        pass

    def write_if(self, label: str) -> None:
        pass

    def write_call(self, name: str, num_args: int) -> None:
        pass

    def write_fn(self, label: str, num_locals: int) -> None:
        pass

    def write_return(self, label: str, num_locals: int) -> None:
        pass
