import pytest
import glob
from subprocess import STDOUT, check_output

from n2t.translator import Parser, VMCommandType, file_strings_to_asm_commands, translator, File


def code_to_misc_file(code: str) -> File:
    return File("anything.txt", code)


def test_parser():
    code = """
        push constant 7
        pop static 3
        add
    """
    parser = Parser(code)
    assert not parser.current()

    assert parser.advance() == "push constant 7"
    assert parser.command_type() == VMCommandType.PUSH
    assert parser.arg1() == "constant"
    assert parser.arg2() == 7
    assert parser.has_more()

    assert parser.advance() == "pop static 3"
    assert parser.command_type() == VMCommandType.POP
    assert parser.arg1() == "static"
    assert parser.arg2() == 3
    assert parser.has_more()

    assert parser.advance() == "add"
    assert parser.command_type() == VMCommandType.ARITHMETIC
    assert parser.arg1() == "add"
    with pytest.raises(Exception):
        parser.arg2()
    assert not parser.has_more()


def test_basic_stack_arithmetic_works():
    code = """
        push constant 7
        push constant 8
        add
    """
    expected_output = ['@7', 'D=A', '@SP', 'A=M', 'M=D', '@SP', 'M=M+1', '@8', 'D=A', '@SP', 'A=M', 'M=D', '@SP',
                       'M=M+1', '@SP', 'M=M-1', 'A=M', 'D=M', '@SP', 'M=M-1', 'A=M', 'M=M+D', '@SP', 'M=M+1']
    assert file_strings_to_asm_commands([code_to_misc_file(code)], write_init=False) == expected_output


@pytest.mark.parametrize("base_folder, test_name, write_init", [
    ["07_tests", "SimpleAdd", False],
    ["07_tests", "StackTest", False],
    ["07_tests", "BasicTest", False],
    ["07_tests", "PointerTest", False],
    ["07_tests", "StaticTest", False],
    ["08_tests", "BasicLoop", False],
    ["08_tests", "FibonacciSeries", False],
    ["08_tests", "SimpleFunction", True],
    ["08_tests", "NestedCall", True],
    ["08_tests", "FibonacciElement", True],
    ["08_tests", "StaticsTest", True],
])
def test_it_passes_translation_tests(base_folder, test_name, write_init):
    code_files = []
    for file in glob.glob(f"n2t/{base_folder}/{test_name}/*.vm"):
        with open(file) as f:
            code_files.append(File(file.split("/")[-1], f.read()))

    output = translator(code_files, write_init=write_init)
    with open(f"n2t/{base_folder}/{test_name}/{test_name}.asm", "w") as f:
        f.write(output)

    cmd = f"local/n2t/tools/CPUEmulator.sh n2t/{base_folder}/{test_name}/{test_name}.tst"
    output = check_output(cmd, shell=True, stderr=STDOUT)
    output = str(output)
    if "End of script - Comparison ended successfully" not in output:
        print('output', output)
        raise Exception(f"{base_folder}/{test_name}/{test_name} script didn't succeed")


@pytest.mark.parametrize("segment, reg_name", [
    ("local", "LCL"),
    ("this", "THIS"),
    ("that", "THAT"),
    ("argument", "ARG"),
])
def test_it_pushes_from_segment(segment, reg_name):
    vm_command = f"push {segment} 5"
    results = file_strings_to_asm_commands([code_to_misc_file(vm_command)], write_init=False)
    assert results == ['@5', 'D=A', f'@{reg_name}', 'A=M', 'A=A+D', 'D=M', '@SP', 'A=M', 'M=D', '@SP', 'M=M+1']


def test_it_pushes_from_temp():
    vm_command = f"push temp 5"
    results = file_strings_to_asm_commands([code_to_misc_file(vm_command)], write_init=False)
    assert results == ['@5', 'D=A', f'@R5', 'A=A+D', 'D=M', '@SP', 'A=M', 'M=D', '@SP', 'M=M+1']


@pytest.mark.parametrize("segment, reg_name", [
    ("local", "LCL"),
    ("this", "THIS"),
    ("that", "THAT"),
    ("argument", "ARG"),
])
def test_it_pops_to_segment(segment, reg_name):
    vm_command = f"pop {segment} 4"
    results = file_strings_to_asm_commands([code_to_misc_file(vm_command)], write_init=False)
    assert results == ['@SP', 'M=M-1', 'A=M', 'D=M', '@R13', 'M=D', '@4', 'D=A', f'@{reg_name}', 'A=M', 'A=A+D', 'D=A',
                       '@R14', 'M=D', '@R13', 'D=M', '@R14', 'A=M', 'M=D']


def test_it_pops_to_temp():
    vm_command = f"pop temp 4"
    results = file_strings_to_asm_commands([code_to_misc_file(vm_command)], write_init=False)
    assert results == ['@SP', 'M=M-1', 'A=M', 'D=M', '@R13', 'M=D', '@4', 'D=A', f'@R5', 'A=A+D', 'D=A',
                       '@R14', 'M=D', '@R13', 'D=M', '@R14', 'A=M', 'M=D']
