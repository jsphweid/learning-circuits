import os
import sys
import pytest
import re
import shutil
from subprocess import check_output, CalledProcessError
from typing import List, NamedTuple

class FileToTest(NamedTuple):
	relative_path: str
	filename: str


def ensure_build_folder_is_reset():
	build_dir = "./build"
	if os.path.exists(build_dir):
		shutil.rmtree(build_dir)
	os.makedirs(build_dir)


def get_test_files() -> List[FileToTest]:
	relevant_paths = []
	for path, _, files in os.walk("./verilog"):
		for name in files:
			if "_test.sv" in name:
				relevant_paths.append(
					FileToTest(os.path.join(path, name), name))
	return relevant_paths


class CompilationException(Exception):
	def __init__(self, *args: object) -> None:
			super().__init__(*args)
	pass


def compile_test_file(test_file: FileToTest) -> str:
	output_path = f"./build/{test_file.filename}.vvp"
	compile_command = f"iverilog -grelative-include -g2012 -o {output_path} {test_file.relative_path}"

	try:
		check_output(compile_command, shell=True)
		return output_path
	except CalledProcessError as e:
		raise CompilationException(e)


def assert_no_errors(compiled_filepath: str):
	simulation_command = ["vvp", compiled_filepath]

	try:
		output = check_output(simulation_command).decode("utf-8")
		assertion_errors = len(re.findall(r'(Error: |ERROR: )', output))
		if assertion_errors > 0:
			raise Exception(output)
	except CalledProcessError as e:
		print(f"Could not assert no errors in {compiled_filepath}", e)
		sys.exit(1)


@pytest.fixture(autouse=True, scope="module")
def setup():
	ensure_build_folder_is_reset()


@pytest.mark.parametrize('file', get_test_files())
def test_file(file):
	compiled_filepath = compile_test_file(file)
	assert_no_errors(compiled_filepath)
