import pytest
from subprocess import STDOUT, check_output, CalledProcessError

from translator import Parser, VMCommandType, file_strings_to_asm_commands, translator


def test_parser():
    code = """
        push constant 7
        pop static 3
        add
    """
    parser = Parser(code)
    assert not parser.current_command()

    assert parser.advance() == "push constant 7"
    assert parser.command_type() == VMCommandType.PUSH
    assert parser.arg1() == "constant"
    assert parser.arg2() == 7
    assert parser.has_more_commands()

    assert parser.advance() == "pop static 3"
    assert parser.command_type() == VMCommandType.POP
    assert parser.arg1() == "static"
    assert parser.arg2() == 3
    assert parser.has_more_commands()

    assert parser.advance() == "add"
    assert parser.command_type() == VMCommandType.ARITHMETIC
    assert parser.arg1() == "add"
    with pytest.raises(Exception):
        parser.arg2()
    assert not parser.has_more_commands()


def test_basic_stack_arithmetic_works():
    code = """
        push constant 7
        push constant 8
        add
    """
    expected_output = ['@7', 'D=A', '@SP', 'A=M', 'M=D', '@SP', 'M=M+1', '@8', 'D=A', '@SP', 'A=M', 'M=D', '@SP',
                       'M=M+1', '@SP', 'M=M-1', 'A=M', 'D=M', '@SP', 'M=M-1', 'A=M', 'M=M+D', '@SP', 'M=M+1']
    assert file_strings_to_asm_commands([code]) == expected_output


@pytest.mark.parametrize("test_folder", [
    "SimpleAdd",
    # "StackTest"
])
def test_it_creates_correct_hack_files(test_folder):
    with open(f"07_tests/{test_folder}/{test_folder}.vm") as f:
        code = f.read()
    output = translator([code])
    with open(f"07_tests/{test_folder}/{test_folder}.asm", "w") as f:
        f.write(output)

    cmd = f"../local/n2t/tools/CPUEmulator.sh ../n2t/07_tests/{test_folder}/{test_folder}.tst"
    output = check_output(cmd, shell=True, stderr=STDOUT)
    output = str(output)
    if "End of script - Comparison ended successfully" not in output:
        print('output', output)
        raise Exception(f"{test_folder} script didn't succeed")
