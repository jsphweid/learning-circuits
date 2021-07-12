import os
import sys
from enum import Enum
from typing import List, Optional, NamedTuple

from n2t.shared import BaseParser, WhiteSpaceStrategy

VM_EXTENSION = ".vm"
ASM_EXTENSION = ".asm"


class File(NamedTuple):
    filename: str
    contents: str

    @property
    def filename_extensionless(self):
        return "".join(self.filename.split(".")[0:-1])


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
    IF_GOTO = 9


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
                "if-goto": VMCommandType.IF_GOTO,
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
    def __init__(self, file: File):
        self._file = file
        self._jump_count = 0

    _increment_stack_pointer = ["@SP", "M=M+1"]
    _decrement_stack_pointer = ["@SP", "M=M-1"]
    _store_value_in_d = ["D=M"]
    _store_addr_in_d = ["D=A"]
    _store_d_at_address = ["M=D"]
    _goto_stack = ["@SP", "A=M"]

    def _get_unique_jump_symbol(self) -> str:
        symbol = f"JUMP{self._jump_count}"
        self._jump_count += 1
        return symbol

    def _write_comparison(self, comparison_instruction: str) -> List[str]:
        jump_symbol = self._get_unique_jump_symbol()
        return CodeWriter._decrement_stack_pointer + ["A=M", "D=M"] + \
               CodeWriter._decrement_stack_pointer + ["A=M", "D=M-D"] + \
               ["M=-1", f"@{jump_symbol}", f"D;{comparison_instruction}"] + \
               ["@SP", "A=M", "M=0", f"({jump_symbol})"] + CodeWriter._increment_stack_pointer

    def _store_value_in_r(self, reg: str, is_addr=False) -> List[str]:
        if reg not in {"R13", "R14", "R15"}:
            raise NotImplementedError
        store = self._store_addr_in_d if is_addr else self._store_value_in_d
        return store + [f"@{reg}", "M=D"]

    def _load_d_from_r(self, reg: str) -> List[str]:
        if reg not in {"R13", "R14", "R15"}:
            raise NotImplementedError
        return [f"@{reg}", "D=M"]

    def _write_and_or(self, symbol: str) -> List[str]:
        return CodeWriter._decrement_stack_pointer + ["A=M", "D=M"] + \
               CodeWriter._decrement_stack_pointer + ["A=M", f"M=M{symbol}D"] + \
               CodeWriter._increment_stack_pointer

    def _write_not_neg(self, symbol: str) -> List[str]:
        return CodeWriter._decrement_stack_pointer + ["A=M", f"M={symbol}M"] + \
               CodeWriter._increment_stack_pointer

    def _write_add_sub(self, symbol: str) -> List[str]:
        return CodeWriter._decrement_stack_pointer + ["A=M", "D=M"] + \
               CodeWriter._decrement_stack_pointer + ["A=M", f"M=M{symbol}D"] + \
               CodeWriter._increment_stack_pointer

    def _goto_segment(self, segment: str, offset=0) -> List[str]:
        mapping = {"this": "THIS", "that": "THAT", "local": "LCL", "argument": "ARG", "temp": "R5", "pointer": "R3",
                   "static": "16"}
        ref = mapping.get(segment, segment)  # if you want to use R12 or whatever you can bypass the mapping
        goto_segment = [f"@{ref}"] if segment == "temp" or segment == "pointer" else [f"@{ref}", "A=M"]
        goto_segment = [f"@{self._file.filename_extensionless}.{offset}"] if segment == "static" else goto_segment
        store_offset = [f"@{offset}", "D=A"] if offset else []
        add_offset = ["A=A+D"] if offset else []
        return store_offset + goto_segment + add_offset

    def write_arithmetic(self, command: str) -> List[str]:
        if command == "add":
            return self._write_add_sub("+")
        elif command == "sub":
            return self._write_add_sub("-")
        elif command == "eq":
            return self._write_comparison("JEQ")
        elif command == "lt":
            return self._write_comparison("JLT")
        elif command == "gt":
            return self._write_comparison("JGT")
        elif command == "and":
            return self._write_and_or("&")
        elif command == "or":
            return self._write_and_or("|")
        elif command == "neg":
            return self._write_not_neg("-")
        elif command == "not":
            return self._write_not_neg("!")
        else:
            raise NotImplementedError

    def write_push_pop(self, command_type: VMCommandType, arg1: str, arg2: int) -> List[str]:
        if command_type == VMCommandType.PUSH:
            if arg1 == "constant":
                return [f"@{arg2}", "D=A", "@SP", "A=M", "M=D"] + CodeWriter._increment_stack_pointer
            elif arg1 in {"this", "that", "local", "argument", "temp", "pointer", "static"}:
                return self._goto_segment(arg1, arg2) + self._store_value_in_d + self._goto_stack + \
                       self._store_d_at_address + self._increment_stack_pointer
            else:
                raise NotImplementedError
        elif command_type == VMCommandType.POP:
            if arg1 in {"this", "that", "local", "argument", "temp", "pointer", "static"}:
                return self._decrement_stack_pointer + ["A=M"] + self._store_value_in_r("R13") + self._goto_segment(
                    arg1, arg2) + \
                       self._store_value_in_r("R14", is_addr=True) + self._load_d_from_r("R13") + \
                       self._goto_segment("R14") + self._store_d_at_address
            else:
                raise NotImplementedError
        else:
            raise NotImplementedError

    @staticmethod
    def write_init() -> List[str]:
        # TODO: vm initialization/bootstrap... gets placed at beginning of the output
        return []

    def write_label(self, label: str) -> List[str]:
        return [f"({label})"]

    def write_goto(self, label: str) -> List[str]:
        return [f"@{label}", "0;JMP"]

    def write_if_goto(self, label: str) -> List[str]:
        return self._decrement_stack_pointer + ["A=M", "D=M", f"@{label}", "D;JNE"]

    def write_call(self):
        pass

    def write_return(self) -> List[str]:
        return []

    def write_function(self, name, num_locals: int) -> List[str]:
        # TODO: this is completely broken
        return [f"({name})"] + self._increment_stack_pointer * num_locals


def file_strings_to_asm_commands(files: List[File]) -> List[str]:
    if len(files) > 1 or not len(files):
        raise NotImplementedError
    parser = Parser(files[0].contents)
    code_writer = CodeWriter(files[0])
    asm_commands = []
    while parser.has_more_commands():
        command = parser.advance()
        if parser.command_type() == VMCommandType.PUSH:
            asm_commands += code_writer.write_push_pop(VMCommandType.PUSH, parser.arg1(), parser.arg2())
        elif parser.command_type() == VMCommandType.POP:
            asm_commands += code_writer.write_push_pop(VMCommandType.POP, parser.arg1(), parser.arg2())
        elif parser.command_type() == VMCommandType.ARITHMETIC:
            asm_commands += code_writer.write_arithmetic(command)
        elif parser.command_type() == VMCommandType.FUNCTION:
            asm_commands += code_writer.write_function(parser.arg1(), parser.arg2())
        elif parser.command_type() == VMCommandType.RETURN:
            asm_commands += code_writer.write_return()
        elif parser.command_type() == VMCommandType.GOTO:
            asm_commands += code_writer.write_goto(parser.arg1())
        elif parser.command_type() == VMCommandType.IF_GOTO:
            asm_commands += code_writer.write_if_goto(parser.arg1())
        elif parser.command_type() == VMCommandType.LABEL:
            asm_commands += code_writer.write_label(parser.arg1())

    return asm_commands


def translator(files: List[File]) -> str:
    init_commands = CodeWriter.write_init()
    asm_commands = init_commands + file_strings_to_asm_commands(files)
    return "\n".join(asm_commands) + "\n"


def read_file_to_str(path: str) -> str:
    with open(path, "r") as f:
        contents = f.read()
    return contents


def get_documents_from_path(path: str) -> List[File]:
    ret: List[File] = []
    # if path is dir, read all vm files
    # if path is file, then assume it's a single vm file
    if os.path.isdir(path):
        # for now, just get files that are direct children of the dir
        for filename in os.listdir(path):
            if VM_EXTENSION in filename and filename[-3:] == VM_EXTENSION:
                path = f"{path}/{filename}"
                ret.append(File(filename, read_file_to_str(path)))
    else:
        filename = path.split("/")[-1]
        ret.append(File(filename, read_file_to_str(path)))
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
