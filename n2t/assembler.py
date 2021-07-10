import sys
from typing import List, Optional
from enum import Enum


class CommandType(Enum):
    A_COMMAND = 0
    C_COMMAND = 1
    L_COMMAND = 2
    INVALID = 3


Command = str


class Parser:
    _raw_file_contents: str

    def __init__(self, raw_file_contents: str) -> None:
        self._raw_file_contents = raw_file_contents
        self._commands = self.parse_instructions()
        self._current_command_index = -1

    def parse_instructions(self) -> List[Command]:
        ret = []
        for line in self._raw_file_contents.split("\n"):
            cleaned_line = self.clean_line(line)
            if cleaned_line:
                ret.append(cleaned_line)
        return ret

    def has_more_commands(self):
        return self._current_command_index + 1 < len(self._commands)

    def advance(self) -> Command:
        self._current_command_index += 1
        return self._commands[self._current_command_index]

    def current_command(self) -> Optional[Command]:
        return self._commands[self._current_command_index] if \
            0 <= self._current_command_index < len(self._commands) else None

    def command_type(self) -> Optional[CommandType]:
        current = self.current_command()
        if current:
            if current[0] == "@" and len(current) > 1:
                return CommandType.A_COMMAND
            elif current[0] == "(" and current[-1] == ")":
                return CommandType.L_COMMAND
            else:
                return CommandType.C_COMMAND

    def symbol(self) -> Optional[str]:
        current = self.current_command()
        if current:
            if self.command_type() == CommandType.A_COMMAND:
                return current[1:]
            elif self.command_type() == CommandType.L_COMMAND:
                return current.replace("(", "").replace(")", "")

    def dest(self) -> Optional[str]:
        current = self.current_command()
        if self.command_type() == CommandType.C_COMMAND \
                and "=" in current:
            return current.split("=")[0]

    def comp(self) -> Optional[str]:
        current = self.current_command()
        if self.command_type() == CommandType.C_COMMAND:
            if "=" in current:
                return current.split("=")[1]
            elif ";" in current:
                return current.split(";")[0]


    def jump(self) -> Optional[str]:
        current = self.current_command()
        if self.command_type() == CommandType.C_COMMAND \
                and ";" in current:
            return current.split(";")[1]

    @staticmethod
    def clean_line(line: str):
        return line.split("//")[0].replace(" ", "").replace("\t", "")


class CodeModule:
    @staticmethod
    def dest(dest: str):
        mapping = {
            None: "000",
            "M": "001",
            "D": "010",
            "MD": "011",
            "A": "100",
            "AM": "101",
            "AD": "110",
            "AMD": "111",
        }
        return mapping[dest]

    @staticmethod
    def jump(jump: str):
        mapping = {
            None: "000",
            "JGT": "001",
            "JEQ": "010",
            "JGE": "011",
            "JLT": "100",
            "JNE": "101",
            "JLE": "110",
            "JMP": "111",
        }
        return mapping[jump]

    @staticmethod
    def comp(comp: str):
        mapping = {
            "0": "0101010",
            "1": "0111111",
            "-1": "0111010",
            "D": "0001100",
            "A": "0110000",
            "!D": "0001101",
            "!A": "0110001",
            "-D": "0001111",
            "-A": "0110011",
            "D+1": "0011111",
            "A+1": "0110111",
            "D-1": "0001110",
            "A-1": "0110010",
            "D+A": "0000010",
            "D-A": "0010011",
            "A-D": "0000111",
            "D&A": "0000000",
            "D|A": "0010101",
            "M": "1110000",
            "!M": "1110001",
            "-M": "1110011",
            "M+1": "1110111",
            "M-1": "1110010",
            "D+M": "1000010",
            "D-M": "1010011",
            "M-D": "1000111",
            "D&M": "1000000",
            "D|M": "1010101"
        }
        return mapping[comp]


def int_str_to_bin(int_str: str, bits=15) -> str:
    return bin(int(int_str))[2:].rjust(bits, "0")


def assemble(code: str) -> str:
    instructions = []
    parser = Parser(code)
    while parser.has_more_commands():
        command = parser.advance()
        if parser.command_type() == CommandType.A_COMMAND:
            instructions.append("0" + int_str_to_bin(command[1:]))
        elif parser.command_type() == CommandType.C_COMMAND:
            comp = CodeModule.comp(parser.comp())
            dest = CodeModule.dest(parser.dest())
            jump = CodeModule.jump(parser.jump())
            instruction = "111" + comp + dest + jump
            instructions.append(instruction)
        else:
            raise NotImplementedError
    return "\n".join(instructions)


if __name__ == '__main__':
    try:
        assert len(sys.argv) == 2
        filepath = sys.argv[1]
        with open(filepath, "r") as f:
            raw_file_contents = f.read()
    except Exception:
        raise Exception("Must have 1 valid filepath argument")

    output = assemble(raw_file_contents)

