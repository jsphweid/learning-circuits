import pytest
from subprocess import STDOUT, check_output

from n2t.translator import Parser, VMCommandType, file_strings_to_asm_commands, translator


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
    "StackTest",
    "BasicTest",
    # "PointerTest",
    # "StaticTest",
])
def test_it_passes_translation_tests(test_folder):
    with open(f"n2t/07_tests/{test_folder}/{test_folder}.vm") as f:
        code = f.read()
    output = translator([code])
    with open(f"n2t/07_tests/{test_folder}/{test_folder}.asm", "w") as f:
        f.write(output)

    cmd = f"local/n2t/tools/CPUEmulator.sh n2t/07_tests/{test_folder}/{test_folder}.tst"
    print('cmd', cmd)
    output = check_output(cmd, shell=True, stderr=STDOUT)
    output = str(output)
    if "End of script - Comparison ended successfully" not in output:
        print('output', output)
        raise Exception(f"{test_folder} script didn't succeed")


@pytest.mark.parametrize("segment, reg_name", [
    ("local", "LCL"),
    ("this", "THIS"),
    ("that", "THAT"),
    ("argument", "ARG"),
])
def test_it_pushes_from_segment(segment, reg_name):
    vm_command = f"push {segment} 5"
    results = file_strings_to_asm_commands([vm_command])
    assert results == ['@5', 'D=A', f'@{reg_name}', 'A=M', 'A=A+D', 'D=M', '@SP', 'A=M', 'M=D', '@SP', 'M=M+1']


def test_it_pushes_from_temp():
    vm_command = f"push temp 5"
    results = file_strings_to_asm_commands([vm_command])
    assert results == ['@5', 'D=A', f'@R5', 'A=A+D', 'D=M', '@SP', 'A=M', 'M=D', '@SP', 'M=M+1']


@pytest.mark.parametrize("segment, reg_name", [
    ("local", "LCL"),
    ("this", "THIS"),
    ("that", "THAT"),
    ("argument", "ARG"),
])
def test_it_pops_to_segment(segment, reg_name):
    vm_command = f"pop {segment} 4"
    results = file_strings_to_asm_commands([vm_command])
    assert results == ['@SP', 'M=M-1', 'A=M', 'D=M', '@R13', 'M=D', '@4', 'D=A', f'@{reg_name}', 'A=M', 'A=A+D', 'D=A',
                       '@R14', 'M=D', '@R13', 'D=M', '@R14', 'A=M', 'M=D']


def test_it_pops_to_temp():
    vm_command = f"pop temp 4"
    results = file_strings_to_asm_commands([vm_command])
    assert results == ['@SP', 'M=M-1', 'A=M', 'D=M', '@R13', 'M=D', '@4', 'D=A', f'@R5', 'A=A+D', 'D=A',
                       '@R14', 'M=D', '@R13', 'D=M', '@R14', 'A=M', 'M=D']
