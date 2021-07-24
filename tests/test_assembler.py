import pytest

from n2t.assembler import Parser, AssemblyCommandType, assemble


def strip_empty_lines(text: str):
    lines = []
    for line in text.split("\n"):
        if line:
            lines.append(line)
    return "\n".join(lines)


def test_parser_has_no_more_commands_if_empty():
    code = ""
    assert not Parser(code).has_more()


def test_parser_has_more_commands_if_at_least_one_command():
    code = "D;JGT"
    assert Parser(code).has_more()


def test_parser_has_more_commands_after_running_a_few_but_not_all():
    code = """
	  @SCREEN
		D=A
		@R1
		M=D
	"""
    parser = Parser(code)
    assert parser.advance() == "@SCREEN"
    assert parser.advance() == "D=A"
    assert parser.has_more()


def test_parser_has_no_more_commands_after_running_through_all():
    code = """
		// test!
	  @SCREEN
		D=A
		(SomeLabel)
		// another test...
	"""
    parser = Parser(code)
    assert parser.advance() == "@SCREEN"
    assert parser.advance() == "D=A"
    assert parser.advance() == "(SomeLabel)"
    assert not parser.has_more()


def test_parser_returns_correct_command_type():
    code = """
		// test!
	  @SCREEN
		D=A
		(SomeLabel)
		// another test...
	"""
    parser = Parser(code)
    parser.advance()
    assert parser.command_type() == AssemblyCommandType.A_COMMAND
    parser.advance()
    assert parser.command_type() == AssemblyCommandType.C_COMMAND
    parser.advance()
    assert parser.command_type() == AssemblyCommandType.L_COMMAND


def test_parser_returns_correct_symbol():
    code = """
		// test!
	  @SCREEN
		D=A
		(SomeLabel)
	"""
    parser = Parser(code)
    parser.advance()
    assert parser.symbol() == "SCREEN"
    parser.advance()
    assert not parser.symbol()
    parser.advance()
    assert parser.symbol() == "SomeLabel"


@pytest.mark.parametrize("command, expected_dest", [
    ("@SCREEN", None),
    ("D=A", "D"),
    ("M=D", "M"),
    ("AMD=D", "AMD"),
    ("A=D", "A"),
    ("AD=M", "AD"),
    ("AM=D", "AM"),
    ("MD=A", "MD"),
    ("A=D", "A"),
    ("0;JMP", None),
    ("D;JGT", None)
])
def test_return_correct_dest(command, expected_dest):
    parser = Parser(command)
    parser.advance()
    assert parser.dest() == expected_dest


@pytest.mark.parametrize("command, expected_comp", [
    ("@SCREEN", None),
    ("D=A", "A"),
    ("M=D", "D"),
    ("AMD=D", "D"),
    ("A=D", "D"),
    ("A=D+1", "D+1")
])
def test_return_correct_comp(command, expected_comp):
    parser = Parser(command)
    parser.advance()
    assert parser.comp() == expected_comp


@pytest.mark.parametrize("command, expected_jump", [
    ("@SCREEN", None),
    ("0;JMP", "JMP"),
    ("D;JGT", "JGT"),
    ("A;JLE", "JLE")
])
def test_return_correct_comp(command, expected_jump):
    parser = Parser(command)
    parser.advance()
    assert parser.jump() == expected_jump


def test_compiled_output_without_symbols():
    instructions = ['M=D', 'D=M', 'D=M-D', 'D;JEQ', '@1', 'A=M', 'M=0', '@23', 'M=M+1', '0;JMP', 'D=M', 'D=M-D', '@50',
                    'D;JEQ', 'A=M', 'M=-1', 'M=M+1', '0;JMP', 'D=A', 'M=D', '0;JMP', 'D=A', 'M=D', '0;JMP', 'D=M',
                    'D;JGT', '0;JMP']
    code = "\n".join(instructions)
    assert assemble(code) == "\n".join(['1110001100001000', '1111110000010000', '1111000111010000', '1110001100000010',
                                        '0000000000000001', '1111110000100000', '1110101010001000', '0000000000010111',
                                        '1111110111001000', '1110101010000111', '1111110000010000', '1111000111010000',
                                        '0000000000110010', '1110001100000010', '1111110000100000', '1110111010001000',
                                        '1111110111001000', '1110101010000111', '1110110000010000', '1110001100001000',
                                        '1110101010000111', '1110110000010000', '1110001100001000', '1110101010000111',
                                        '1111110000010000', '1110001100000001', '1110101010000111', ''])


@pytest.mark.parametrize("file, expected_output_file", [
    ("Add.asm", "Add.hack"),
    ("Max.asm", "Max.hack"),
    ("MaxL.asm", "MaxL.hack"),
    ("Pong.asm", "Pong.hack"),
    ("PongL.asm", "PongL.hack"),
    ("Rect.asm", "Rect.hack"),
    ("RectL.asm", "RectL.hack"),
])
def test_it_creates_correct_hack_files(file, expected_output_file):
    with open(f"n2t/06_tests/truth_asm/{file}") as f:
        code = f.read()
    with open(f"n2t/06_tests/truth_hack/{expected_output_file}") as f:
        expected_output = f.read()
    assert assemble(code) == expected_output
