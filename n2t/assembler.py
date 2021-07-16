import sys
from typing import List, Optional, Dict
from enum import Enum

from n2t.shared import Command, BaseParser, WhiteSpaceStrategy


class AssemblyCommandType(Enum):
    A_COMMAND = 0
    C_COMMAND = 1
    L_COMMAND = 2
    INVALID = 3


class Parser(BaseParser):
    _commands = List[Command]

    def __init__(self, raw_file_contents: str) -> None:
        super().__init__(raw_file_contents, WhiteSpaceStrategy.ELIMINATE_ALL)

    def command_type(self) -> Optional[AssemblyCommandType]:
        current = self.current()
        if current:
            if current[0] == "@" and len(current) > 1:
                return AssemblyCommandType.A_COMMAND
            elif current[0] == "(" and current[-1] == ")":
                return AssemblyCommandType.L_COMMAND
            else:
                return AssemblyCommandType.C_COMMAND

    def symbol(self) -> Optional[str]:
        current = self.current()
        if current:
            if self.command_type() == AssemblyCommandType.A_COMMAND:
                return current[1:]
            elif self.command_type() == AssemblyCommandType.L_COMMAND:
                return current.replace("(", "").replace(")", "")

    def dest(self) -> Optional[str]:
        current = self.current()
        if self.command_type() == AssemblyCommandType.C_COMMAND \
                and "=" in current:
            return current.split("=")[0]

    def comp(self) -> Optional[str]:
        current = self.current()
        if self.command_type() == AssemblyCommandType.C_COMMAND:
            if "=" in current:
                return current.split("=")[1]
            elif ";" in current:
                return current.split(";")[0]

    def jump(self) -> Optional[str]:
        current = self.current()
        if self.command_type() == AssemblyCommandType.C_COMMAND \
                and ";" in current:
            return current.split(";")[1]

    def command_is_a_and_symbol(self):
        try:
            int(self.symbol())
            # If it can be parsed as an int, it's not really a symbol, but a number
            # TODO: maybe the self.symbol() fn shouldn't return a number if it's named `symbol`...
            return False
        except:
            return True


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


class SymbolTable:
    _table: Dict[str, int]

    def __init__(self):
        self._table = {}
        r_symbols = [(f"R{i}", i) for i in range(16)]
        other_symbols = [("SP", 0), ("LCL", 1), ("ARG", 2), ("THIS", 3), ("THAT", 4), ("SCREEN", 16384), ("KBD", 24576)]
        predefined_symbols = r_symbols + other_symbols
        for item in predefined_symbols:
            key, value = item
            self._table[key] = value

    def contains(self, symbol: str) -> bool:
        return self._table.get(symbol) is not None

    def add_entry(self, symbol: str, addr: int) -> None:
        if self.contains(symbol):
            raise Exception(f"Can't add {symbol} symbol table because it already exists")
        self._table[symbol] = addr

    def get_address(self, symbol: str) -> Optional[int]:
        return self._table.get(symbol)


def int_str_to_bin(int_str: str, bits=15) -> str:
    return bin(int(int_str))[2:].rjust(bits, "0")


def assemble(code: str) -> str:
    # first pass - build symbol table
    symbol_table = SymbolTable()
    parser = Parser(code)
    current_rom_address = 0
    while parser.has_more():
        parser.advance()
        if parser.command_type() == AssemblyCommandType.L_COMMAND:
            symbol_table.add_entry(parser.symbol(), current_rom_address)
        if parser.command_type() == AssemblyCommandType.A_COMMAND or parser.command_type() == AssemblyCommandType.C_COMMAND:
            current_rom_address += 1

    # second pass - finalize instructions
    instructions = []
    parser = Parser(code)
    next_unused_ram_address = 16
    while parser.has_more():
        command = parser.advance()
        if parser.command_type() == AssemblyCommandType.A_COMMAND:
            if parser.command_is_a_and_symbol():
                symbol = parser.symbol()
                if symbol_table.contains(symbol):
                    addr = str(symbol_table.get_address(symbol))
                    instructions.append("0" + int_str_to_bin(addr))
                else:
                    symbol_table.add_entry(symbol, next_unused_ram_address)
                    instructions.append("0" + int_str_to_bin(str(next_unused_ram_address)))
                    next_unused_ram_address += 1
            else:
                instructions.append("0" + int_str_to_bin(command[1:]))
        elif parser.command_type() == AssemblyCommandType.C_COMMAND:
            comp = CodeModule.comp(parser.comp())
            dest = CodeModule.dest(parser.dest())
            jump = CodeModule.jump(parser.jump())
            instruction = "111" + comp + dest + jump
            instructions.append(instruction)
        elif parser.command_type() == AssemblyCommandType.L_COMMAND:
            pass
    return "\n".join(instructions) + "\n"


if __name__ == '__main__':
    try:
        assert len(sys.argv) == 3
        filepath = sys.argv[1]
        destination_filepath = sys.argv[2]
        with open(filepath, "r") as f:
            raw_file_contents = f.read()
    except Exception:
        raise Exception("Must have 2 valid filepath arguments")

    output = assemble(raw_file_contents)

    with open(destination_filepath, 'w') as file:
        file.write(output)
