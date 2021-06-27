import os
import sys
import pytest
import re
import shutil
from subprocess import check_output, CalledProcessError
from typing import List, NamedTuple


class TestFile(NamedTuple):
	relative_path: str
	filename: str


def ensure_build_folder_is_reset():
	build_dir = "./build"
	if os.path.exists(build_dir):
		shutil.rmtree(build_dir)
	os.makedirs(build_dir)


def get_test_files() -> List[TestFile]:
	relevant_paths = []
	for path, _, files in os.walk("./verilog"):
		for name in files:
			if "_test.sv" in name:
				relevant_paths.append(
					TestFile(os.path.join(path, name), name))
	return relevant_paths


def run_test_file(test_file: TestFile):
	# compile
	output_path = f"./build/{test_file.filename}.vvp"
	compile_command = f"iverilog -grelative-include -g2012 -o {output_path} {test_file.relative_path}"

	try:
		what = check_output(compile_command, shell=True)
	except CalledProcessError as e:
		print(f"Could not compile verilog test {test_file.relative_path}", e)
		sys.exit(1)

	# simulate
	simulation_command = ["vvp", output_path]

	try:
		output = check_output(simulation_command).decode("utf-8")
		assertion_errors = len(re.findall(r'(Error: |ERROR: )', output))
		print(output)
		# color = Fore.YELLOW if assertion_errors > 0 else Fore.GREEN
		print("Found " + str(assertion_errors) + " assertion errors in " + test_file.filename)
		# return {"assertion_errors": assertion_errors, "run_errors": 0}
	except CalledProcessError as e:
		print(f"Could not run verilog test {output_path}", e)
		sys.exit(1)


if __name__ == "__main__":
	ensure_build_folder_is_reset()
	test_files = get_test_files()
	for test_file in test_files:
		run_test_file(test_file)