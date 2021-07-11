import os
import sys
from enum import Enum
from typing import List, Optional

from n2t.shared import BaseParser, WhiteSpaceStrategy

VM_EXTENSION = ".vm"
ASM_EXTENSION = ".asm"


class VMCommandType(Enum):
    ARITHMETIC = 0
    PUSH = 1
    POP = 2
    LABEL = 3
    GOTO = 4
    IF = 5
    FUNCTION = 6
    RETURN = 7
    CALL = 8


class Parser(BaseParser):
    def __init__(self, raw_file_contents: str):
        super().__init__(raw_file_contents, WhiteSpaceStrategy.MAX_ONE_IN_BETWEEN_WORDS)

    def command_type(self) -> Optional[VMCommandType]:
        current = self.current_command()
        if current:
            mapping = {
                "add": VMCommandType.ARITHMETIC,
                "sub": VMCommandType.ARITHMETIC,
                "neg": VMCommandType.ARITHMETIC,
                "eq": VMCommandType.ARITHMETIC,
                "gt": VMCommandType.ARITHMETIC,
                "lt": VMCommandType.ARITHMETIC,
                "and": VMCommandType.ARITHMETIC,
                "or": VMCommandType.ARITHMETIC,
                "not": VMCommandType.ARITHMETIC,
                "push": VMCommandType.PUSH,
                "pop": VMCommandType.POP,
                "label": VMCommandType.LABEL,
                "goto": VMCommandType.GOTO,
                "return": VMCommandType.RETURN,
                "function": VMCommandType.FUNCTION,
                "call": VMCommandType.CALL,
            }
            first_word = current.split(" ")[0]  # this is guaranteed
            command_type = mapping.get(first_word)
            if not command_type:
                raise NotImplementedError(f"Command `{command_type}` is invalid or not implemented")
            return command_type

    def arg1(self) -> Optional[str]:
        if self.current_command():
            if self.command_type == VMCommandType.RETURN:
                raise Exception("Shouldn't have called arg1 when the command is a `return` type...")
            elif self.command_type() == VMCommandType.ARITHMETIC:
                return self.current_command()  # should be either `add` or `sub`
            else:
                return self.current_command().split(" ")[1]

    def arg2(self) -> Optional[int]:
        if self.current_command():
            if self.command_type() in [
                VMCommandType.PUSH,
                VMCommandType.POP,
                VMCommandType.FUNCTION,
                VMCommandType.CALL,
            ]:
                return int(self.current_command().split(" ")[2])
            else:
                raise Exception(f"Shouldn't not have requested arg2 for command `{self.current_command()}`")


class CodeWriter:
    increment_stack_pointer = ["@SP", "M=M+1"]
    decrement_stack_pointer = ["@SP", "M=M-1"]

    @staticmethod
    def writeArithmetic(command: str) -> List[str]:
        if command == "add":
            return CodeWriter.decrement_stack_pointer + ["A=M", "D=M"] + \
                   CodeWriter.decrement_stack_pointer + ["A=M", "M=M+D"] + \
                   CodeWriter.increment_stack_pointer
        else:
            raise NotImplementedError

    @staticmethod
    def writePushPop(command_type: VMCommandType, arg1: str, arg2: int) -> List[str]:
        if command_type == VMCommandType.PUSH:
            if arg1 == "constant":
                return [f"@{arg2}", "D=A", "@SP", "A=M", "M=D"] + CodeWriter.increment_stack_pointer
            else:
                raise NotImplementedError
        else:
            raise NotImplementedError


def file_strings_to_asm_commands(files: List[str]) -> List[str]:
    if len(files) > 1 or not len(files):
        raise NotImplementedError
    parser = Parser(files[0])
    asm_commands = []
    while parser.has_more_commands():
        command = parser.advance()
        if parser.command_type() == VMCommandType.PUSH:
            asm_commands += CodeWriter.writePushPop(VMCommandType.PUSH, parser.arg1(), parser.arg2())
        if parser.command_type() == VMCommandType.ARITHMETIC:
            asm_commands += CodeWriter.writeArithmetic(command)

    return asm_commands


def translator(files: List[str]) -> str:
    asm_commands = file_strings_to_asm_commands(files)
    return "\n".join(asm_commands) + "\n"


def read_file_to_str(path: str) -> str:
    with open(path, "r") as f:
        contents = f.read()
    return contents


def get_documents_from_path(path: str) -> List[str]:
    ret = []
    # if path is dir, read all vm files
    # if path is file, then assume it's a single vm file
    if os.path.isdir(path):
        # for now, just get files that are direct children of the dir
        for file in os.listdir(path):
            if VM_EXTENSION in file and file[-3:] == VM_EXTENSION:
                ret.append(read_file_to_str(f"{path}/{file}"))
    else:
        ret.append(read_file_to_str(path))
    return ret


if __name__ == "__main__":
    try:
        assert len(sys.argv) == 3
        file_or_dir = sys.argv[1]
        documents = get_documents_from_path(file_or_dir)
        destination_filepath = sys.argv[2]
    except Exception:
        raise Exception("Must have 2 valid filepath arguments")

    output = translator(documents)

    with open(destination_filepath, 'w') as file:
        file.write(output)
