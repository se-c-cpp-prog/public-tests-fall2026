#!/usr/bin/env python3

import sys
import os

import testbuild

import Utils

from typing import Union, Iterable, List, Dict, Any, Optional
from dataclasses import dataclass
from pathlib import Path

__TARGET_NAME = "MiniTerminal"
__CATEGORIES_TO_ENVIROMENT_MAPPER = {
	"help": "HELP",
	"exit": "EXIT",
	"cat": "CAT",
	"wc": "WC",
	"paste": "PASTE",
	"sort": "SORT",
	"diff": "DIFF",
	"neg": "NEG",
}

__BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "testdata", "mini_terminal")
__INPUT_DIR = os.path.join(__BASE_DIR, "input")
__OUTPUT_DIR = os.path.join(__BASE_DIR, "output")
__REFERENCE_DIR = os.path.join(__BASE_DIR, "reference")
__DATA_DIR = os.path.join(__BASE_DIR, "data")

__ERROR_SUCCESS = 0
__ERROR_CANNOT_OPEN_FILE = 1
__ERROR_OUT_OF_MEMORY = 2
__ERROR_DATA_INVALID = 3
__ERROR_ARGUMENTS_INVALID = 4

@dataclass
class BatchTestData:
	name: str
	input_filename: str
	output_filename: str
	reference_filename: str
	returncode_policy: testbuild.ReturnCodePolicy
	returncode: int
	timeout: float
	category: str

class __BatchExpected(testbuild.Expected):
	def __init__(self, output_filename: str, reference_filename: str) -> None:
		self.__output_filename = output_filename
		self.__reference_filename = reference_filename

	def test(self, run: testbuild.Run, runned: testbuild.Runned) -> testbuild.CheckReturn:
		workdir = runned.get_workdir()

		input_file = None
		args = list(run.args)
		for i, arg in enumerate(args):
			if arg == "--input" and i + 1 < len(args):
				input_file = args[i + 1]
				break

		if not input_file:
			return testbuild.Verdict(
				testbuild.VerdictCode.EXPECTATION,
				"no --input argument found"
			)

		import subprocess
		result = subprocess.run(
			[runned.executable, "--input", input_file],
			cwd=workdir,
			capture_output=True,
			text=True,
			timeout=10,
		)
		actual = result.stdout.strip()

		reference = Path(self.__reference_filename).read_text(encoding="utf-8").strip()

		if actual != reference:
			return testbuild.Verdict(
				testbuild.VerdictCode.EXPECTATION,
				f"output mismatch\n--- expected (reference) ---\n{reference}\n--- actual (output) ---\n{actual}"
			)
		return testbuild.OK

def __get_tester() -> testbuild.Tester:
	tester = testbuild.Tester(__TARGET_NAME, coefficients = Utils.get_coefficients(__TARGET_NAME, __CATEGORIES_TO_ENVIROMENT_MAPPER))

	__BATCH_SEED = os.path.join(__BASE_DIR, "batch_data")
	__INPUT_DIR_ABS = os.path.realpath(__INPUT_DIR)
	__BATCH_SEED_ABS = os.path.realpath(__BATCH_SEED)

	with tester.group("help batch", categories = ["help"]) as group:
		for f in ["help_1.txt", "help_2.txt"]:
			input_path = os.path.join(__INPUT_DIR_ABS, f)
			if not os.path.exists(input_path):
				continue
			output_path = f.replace(".txt", "_out.txt")
			ref_path = os.path.join(__REFERENCE_DIR, output_path)
			with group.test(f"batch {f}", seed_directory = __BATCH_SEED_ABS) as test:
				test.args = ["--input", input_path, "--output", output_path]
				test.expected = __BatchExpected(output_path, ref_path)
				test.returncode_policy = testbuild.ReturnCodePolicy.SHOULD_BE_ZERO
				test.timeout = 5.0

	with tester.group("exit batch", categories = ["exit"]) as group:
		input_path = os.path.join(__INPUT_DIR_ABS, "exit_1.txt")
		if os.path.exists(input_path):
			output_path = "exit_1_out.txt"
			ref_path = os.path.join(__REFERENCE_DIR, output_path)
			with group.test("batch exit", seed_directory = __BATCH_SEED_ABS) as test:
				test.args = ["--input", input_path, "--output", output_path]
				test.expected = __BatchExpected(output_path, ref_path)
				test.returncode_policy = testbuild.ReturnCodePolicy.SHOULD_BE_ZERO
				test.timeout = 5.0

	with tester.group("cat batch", categories = ["cat"]) as group:
		for f in ["cat_1.txt", "cat_2.txt", "cat_3.txt"]:
			input_path = os.path.join(__INPUT_DIR_ABS, f)
			if not os.path.exists(input_path):
				continue
			output_path = f.replace(".txt", "_out.txt")
			ref_path = os.path.join(__REFERENCE_DIR, output_path)
			with group.test(f"batch {f}", seed_directory = __BATCH_SEED_ABS) as test:
				test.args = ["--input", input_path, "--output", output_path]
				test.expected = __BatchExpected(output_path, ref_path)
				test.returncode_policy = testbuild.ReturnCodePolicy.SHOULD_BE_ZERO
				test.timeout = 5.0

	with tester.group("wc batch", categories = ["wc"]) as group:
		for f in ["wc_1.txt", "wc_2.txt"]:
			input_path = os.path.join(__INPUT_DIR_ABS, f)
			if not os.path.exists(input_path):
				continue
			output_path = f.replace(".txt", "_out.txt")
			ref_path = os.path.join(__REFERENCE_DIR, output_path)
			with group.test(f"batch {f}", seed_directory = __BATCH_SEED_ABS) as test:
				test.args = ["--input", input_path, "--output", output_path]
				test.expected = __BatchExpected(output_path, ref_path)
				test.returncode_policy = testbuild.ReturnCodePolicy.SHOULD_BE_ZERO
				test.timeout = 5.0

	with tester.group("sort batch", categories = ["sort"]) as group:
		for f in ["sort_1.txt", "sort_2.txt"]:
			input_path = os.path.join(__INPUT_DIR_ABS, f)
			if not os.path.exists(input_path):
				continue
			output_path = f.replace(".txt", "_out.txt")
			ref_path = os.path.join(__REFERENCE_DIR, output_path)
			with group.test(f"batch {f}", seed_directory = __BATCH_SEED_ABS) as test:
				test.args = ["--input", input_path, "--output", output_path]
				test.expected = __BatchExpected(output_path, ref_path)
				test.returncode_policy = testbuild.ReturnCodePolicy.SHOULD_BE_ZERO
				test.timeout = 5.0

	with tester.group("diff batch", categories = ["diff"]) as group:
		input_path = os.path.join(__INPUT_DIR_ABS, "diff_1.txt")
		if os.path.exists(input_path):
			output_path = "diff_1_out.txt"
			ref_path = os.path.join(__REFERENCE_DIR, output_path)
			with group.test("batch diff equal", seed_directory = __BATCH_SEED_ABS) as test:
				test.args = ["--input", input_path, "--output", output_path]
				test.expected = __BatchExpected(output_path, ref_path)
				test.returncode_policy = testbuild.ReturnCodePolicy.SHOULD_BE_ZERO
				test.timeout = 5.0

	with tester.group("paste batch", categories = ["paste"]) as group:
		input_path = os.path.join(__INPUT_DIR_ABS, "paste_1.txt")
		if os.path.exists(input_path):
			output_path = "paste_1_out.txt"
			ref_path = os.path.join(__REFERENCE_DIR, output_path)
			with group.test("batch paste", seed_directory = __BATCH_SEED_ABS) as test:
				test.args = ["--input", input_path, "--output", output_path]
				test.expected = __BatchExpected(output_path, ref_path)
				test.returncode_policy = testbuild.ReturnCodePolicy.SHOULD_BE_ZERO
				test.timeout = 5.0

	with tester.group("cat interactive", categories = ["cat"]) as group:
		# Create temporary test file in workdir
		with group.test("cat basic") as test:
			with test.before_test() as hooks:
				hooks.create_file("test_input.txt", "line1\nline2\nline3\n")
			test.interactive([
				testbuild.InteractiveStep(
					input_line="cat --path test_input.txt",
					expect_stdout=lambda s: True if s == "line1\nline2\nline3\n" else '"line1\\nline2\\nline3\\n" in stdout'
				),
				testbuild.InteractiveStep(input_line="exit"),
			])
			test.returncode_policy = testbuild.ReturnCodePolicy.SHOULD_BE_ZERO

		with group.test("cat --head") as test:
			with test.before_test() as hooks:
				hooks.create_file("test_input.txt", "aaa\nbbb\nccc\nddd\neee\n")
			test.interactive([
				testbuild.InteractiveStep(
					input_line="cat --path test_input.txt --head 2",
					expect_stdout=lambda s: True if "aaa" in s and "bbb" in s and "ccc" not in s else '"aaa" and "bbb" in stdout and "ccc" not in stdout'
				),
				testbuild.InteractiveStep(input_line="exit"),
			])
			test.returncode_policy = testbuild.ReturnCodePolicy.SHOULD_BE_ZERO

		with group.test("cat --tail") as test:
			with test.before_test() as hooks:
				hooks.create_file("test_input.txt", "aaa\nbbb\nccc\nddd\neee\n")
			test.interactive([
				testbuild.InteractiveStep(
					input_line="cat --path test_input.txt --tail 2",
					expect_stdout=lambda s: True if s.strip().split("\n") == ["ddd", "eee"] else '["ddd", "eee"] in stdout'
				),
				testbuild.InteractiveStep(input_line="exit"),
			])
			test.returncode_policy = testbuild.ReturnCodePolicy.SHOULD_BE_ZERO

		with group.test("cat --print_width") as test:
			with test.before_test() as hooks:
				hooks.create_file("test_input.txt", "abcdefghij\n")
			test.interactive([
				testbuild.InteractiveStep(
					input_line="cat --path test_input.txt --print_width 3",
					expect_stdout=lambda s: True if "abc" in s and "def" in s and "ghi" in s and "j" in s else '"abc", "def", "ghi", "j" in stdout'
				),
				testbuild.InteractiveStep(input_line="exit"),
			])
			test.returncode_policy = testbuild.ReturnCodePolicy.SHOULD_BE_ZERO

		with group.test("cat head and tail together (error)") as test:
			test.interactive([
				testbuild.InteractiveStep(
					input_line="cat --path nonexistent.txt --head 1 --tail 1",
					expect_stdout=lambda s: "ERROR" in s if "ERROR" in s else "ERROR in stdout"
				),
				testbuild.InteractiveStep(input_line="exit"),
			])
			test.returncode = __ERROR_DATA_INVALID

	with tester.group("wc interactive", categories = ["wc"]) as group:
		with group.test("wc basic") as test:
			with test.before_test() as hooks:
				hooks.create_file("test_input.txt", "word1 word2\nword3\n")
			test.interactive([
				testbuild.InteractiveStep(
					input_line="wc test_input.txt",
					expect_stdout=lambda s: True if s.strip().split("\t") == ["2", "3", "18"] else '["2", "3", "18"] in stdout'
				),
				testbuild.InteractiveStep(input_line="exit"),
			])
			test.returncode_policy = testbuild.ReturnCodePolicy.SHOULD_BE_ZERO

		with group.test("wc -l -w -c") as test:
			with test.before_test() as hooks:
				hooks.create_file("test_input.txt", "ab\n")
			test.interactive([
				testbuild.InteractiveStep(
					input_line="wc test_input.txt -l -w -c",
					expect_stdout=lambda s: True if s.strip().split("\t") == ["1", "1", "3"] else '["1", "1", "3"] in stdout'
				),
				testbuild.InteractiveStep(input_line="exit"),
			])
			test.returncode_policy = testbuild.ReturnCodePolicy.SHOULD_BE_ZERO

		with group.test("wc empty file") as test:
			with test.before_test() as hooks:
				hooks.create_file("test_input.txt", "")
			test.interactive([
				testbuild.InteractiveStep(
					input_line="wc test_input.txt",
					expect_stdout=lambda s: "0" in s if "0" in s else "0 in stdout"
				),
				testbuild.InteractiveStep(input_line="exit"),
			])
			test.returncode_policy = testbuild.ReturnCodePolicy.SHOULD_BE_ZERO

	with tester.group("sort interactive", categories = ["sort"]) as group:
		with group.test("sort basic") as test:
			with test.before_test() as hooks:
				hooks.create_file("test_input.txt", "3\n1\n4\n1\n5\n")
			test.interactive([
				testbuild.InteractiveStep(
					input_line="sort test_input.txt",
					expect_stdout=lambda s: True if s.strip().split("\n") == sorted(s.strip().split("\n")) else 'sorted output'
				),
				testbuild.InteractiveStep(input_line="exit"),
			])
			test.returncode_policy = testbuild.ReturnCodePolicy.SHOULD_BE_ZERO

		with group.test("sort --num") as test:
			with test.before_test() as hooks:
				hooks.create_file("test_input.txt", "10\n2\n1\n20\n")
			test.interactive([
				testbuild.InteractiveStep(
					input_line="sort test_input.txt --num",
					expect_stdout=lambda s: True if "1\n2\n10\n20" in s else '"1\\n2\\n10\\n20" in stdout'
				),
				testbuild.InteractiveStep(input_line="exit"),
			])
			test.returncode_policy = testbuild.ReturnCodePolicy.SHOULD_BE_ZERO

		with group.test("sort --reverse") as test:
			with test.before_test() as hooks:
				hooks.create_file("test_input.txt", "1\n2\n3\n")
			test.interactive([
				testbuild.InteractiveStep(
					input_line="sort test_input.txt --reverse",
					expect_stdout=lambda s: True if "3\n2\n1" in s else '"3\\n2\\n1" in stdout'
				),
				testbuild.InteractiveStep(input_line="exit"),
			])
			test.returncode_policy = testbuild.ReturnCodePolicy.SHOULD_BE_ZERO

		with group.test("sort --unique") as test:
			with test.before_test() as hooks:
				hooks.create_file("test_input.txt", "1\n2\n1\n3\n2\n")
			test.interactive([
				testbuild.InteractiveStep(
					input_line="sort test_input.txt --unique",
					expect_stdout=lambda s: True if s.strip() == "1\n2\n3" else '"1\\n2\\n3" in stdout'
				),
				testbuild.InteractiveStep(input_line="exit"),
			])
			test.returncode_policy = testbuild.ReturnCodePolicy.SHOULD_BE_ZERO

		with group.test("sort --ignore_case") as test:
			with test.before_test() as hooks:
				hooks.create_file("test_input.txt", "b\nA\nc\na\n")
			test.interactive([
				testbuild.InteractiveStep(
					input_line="sort test_input.txt --ignore_case",
					expect_stdout=lambda s: True if "A" in s and "a" in s else '"A" and "a" in stdout'
				),
				testbuild.InteractiveStep(input_line="exit"),
			])
			test.returncode_policy = testbuild.ReturnCodePolicy.SHOULD_BE_ZERO

		with group.test("sort --range") as test:
			with test.before_test() as hooks:
				hooks.create_file("test_input.txt", "z\nb\na\nc\ny\n")
			test.interactive([
				testbuild.InteractiveStep(
					input_line="sort test_input.txt --range 1,3",
					expect_stdout=lambda s: "z" in s if "z" in s else "z in stdout"
				),
				testbuild.InteractiveStep(input_line="exit"),
			])
			test.returncode_policy = testbuild.ReturnCodePolicy.SHOULD_BE_ZERO

	with tester.group("diff interactive", categories = ["diff"]) as group:
		with group.test("diff different files") as test:
			with test.before_test() as hooks:
				hooks.create_file("file_a.txt", "abc\nb\n123\n")
				hooks.create_file("file_b.txt", "abc\nc\n231\n")
			test.interactive([
				testbuild.InteractiveStep(
					input_line="diff file_a.txt file_b.txt",
					expect_stdout=lambda s: True if "-" in s and "+" in s else '"- N" and "+ M" in stdout'
				),
				testbuild.InteractiveStep(input_line="exit"),
			])
			test.returncode_policy = testbuild.ReturnCodePolicy.SHOULD_BE_ZERO

		with group.test("diff --all same files") as test:
			with test.before_test() as hooks:
				hooks.create_file("file_a.txt", "abc\ndef\n")
				hooks.create_file("file_b.txt", "abc\ndef\n")
			test.interactive([
				testbuild.InteractiveStep(
					input_line="diff --all file_a.txt file_b.txt",
					expect_stdout=lambda s: "=" in s if "=" in s else "= N in stdout"
				),
				testbuild.InteractiveStep(input_line="exit"),
			])
			test.returncode_policy = testbuild.ReturnCodePolicy.SHOULD_BE_ZERO

		with group.test("diff -b binary mode") as test:
			with test.before_test() as hooks:
				hooks.create_file("file_a.txt", "ab\n")
				hooks.create_file("file_b.txt", "ac\n")
			test.interactive([
				testbuild.InteractiveStep(
					input_line="diff -b file_a.txt file_b.txt",
					expect_stdout=lambda s: "0x" in s.lower() if "0x" in s.lower() else "0x in stdout"
				),
				testbuild.InteractiveStep(input_line="exit"),
			])
			test.returncode_policy = testbuild.ReturnCodePolicy.SHOULD_BE_ZERO

	with tester.group("paste interactive", categories = ["paste"]) as group:
		with group.test("paste basic") as test:
			with test.before_test() as hooks:
				hooks.create_file("col1.txt", "one\ntwo\nthree\n")
				hooks.create_file("col2.txt", "1\n2\n3\n")
			test.interactive([
				testbuild.InteractiveStep(
					input_line="paste col1.txt col2.txt",
					expect_stdout=lambda s: True if "one" in s and "1" in s else '"one" and "1" in stdout'
				),
				testbuild.InteractiveStep(input_line="exit"),
			])
			test.returncode_policy = testbuild.ReturnCodePolicy.SHOULD_BE_ZERO

		with group.test("paste -d colon") as test:
			with test.before_test() as hooks:
				hooks.create_file("col1.txt", "one\ntwo\n")
				hooks.create_file("col2.txt", "1\n2\n")
			test.interactive([
				testbuild.InteractiveStep(
					input_line="paste -d : col1.txt col2.txt",
					expect_stdout=lambda s: "one:1" in s if "one:1" in s else "one:1 in stdout"
				),
				testbuild.InteractiveStep(input_line="exit"),
			])
			test.returncode_policy = testbuild.ReturnCodePolicy.SHOULD_BE_ZERO

		with group.test("paste -s") as test:
			with test.before_test() as hooks:
				hooks.create_file("col1.txt", "one\ntwo\n")
				hooks.create_file("col2.txt", "1\n2\n")
			test.interactive([
				testbuild.InteractiveStep(
					input_line="paste -s col1.txt col2.txt",
					expect_stdout=lambda s: True if "one" in s and "two" in s else '"one" and "two" in stdout'
				),
				testbuild.InteractiveStep(input_line="exit"),
			])
			test.returncode_policy = testbuild.ReturnCodePolicy.SHOULD_BE_ZERO

	with tester.group("negative interactive", categories = ["neg"]) as group:
		with group.test("unknown command") as test:
			test.interactive([
				testbuild.InteractiveStep(
					input_line="foo",
					expect_stdout=lambda s: "ERROR" in s if "ERROR" in s else "ERROR in stdout"
				),
				testbuild.InteractiveStep(input_line="exit"),
			])
			test.returncode_policy = testbuild.ReturnCodePolicy.SHOULD_NOT_BE_ZERO
			test.returncode = __ERROR_DATA_INVALID

		with group.test("cat missing path") as test:
			test.interactive([
				testbuild.InteractiveStep(
					input_line="cat",
					expect_stdout=lambda s: "ERROR" in s if "ERROR" in s else "ERROR in stdout"
				),
				testbuild.InteractiveStep(input_line="exit"),
			])
			test.returncode_policy = testbuild.ReturnCodePolicy.SHOULD_NOT_BE_ZERO
			test.returncode = __ERROR_ARGUMENTS_INVALID

		with group.test("cat non-existent file") as test:
			test.interactive([
				testbuild.InteractiveStep(
					input_line="cat --path /nonexistent_file_xyz.txt",
					expect_stdout=lambda s: "ERROR" in s if "ERROR" in s else "ERROR in stdout"
				),
				testbuild.InteractiveStep(input_line="exit"),
			])
			test.returncode_policy = testbuild.ReturnCodePolicy.SHOULD_NOT_BE_ZERO
			test.returncode = __ERROR_CANNOT_OPEN_FILE

		with group.test("cat head+tail together") as test:
			with test.before_test() as hooks:
				hooks.create_file("test.txt", "a\nb\n")
			test.interactive([
				testbuild.InteractiveStep(
					input_line="cat --path test.txt --head 1 --tail 1",
					expect_stdout=lambda s: "ERROR" in s if "ERROR" in s else "ERROR in stdout"
				),
				testbuild.InteractiveStep(input_line="exit"),
			])
			test.returncode_policy = testbuild.ReturnCodePolicy.SHOULD_NOT_BE_ZERO
			test.returncode = __ERROR_DATA_INVALID

		with group.test("wc missing path") as test:
			test.interactive([
				testbuild.InteractiveStep(
					input_line="wc",
					expect_stdout=lambda s: "ERROR" in s if "ERROR" in s else "ERROR in stdout"
				),
				testbuild.InteractiveStep(input_line="exit"),
			])
			test.returncode_policy = testbuild.ReturnCodePolicy.SHOULD_NOT_BE_ZERO
			test.returncode = __ERROR_ARGUMENTS_INVALID

		with group.test("sort missing path") as test:
			test.interactive([
				testbuild.InteractiveStep(
					input_line="sort",
					expect_stdout=lambda s: "ERROR" in s if "ERROR" in s else "ERROR in stdout"
				),
				testbuild.InteractiveStep(input_line="exit"),
			])
			test.returncode_policy = testbuild.ReturnCodePolicy.SHOULD_NOT_BE_ZERO
			test.returncode = __ERROR_ARGUMENTS_INVALID

		with group.test("diff missing paths") as test:
			test.interactive([
				testbuild.InteractiveStep(
					input_line="diff",
					expect_stdout=lambda s: "ERROR" in s if "ERROR" in s else "ERROR in stdout"
				),
				testbuild.InteractiveStep(input_line="exit"),
			])
			test.returncode_policy = testbuild.ReturnCodePolicy.SHOULD_NOT_BE_ZERO
			test.returncode = __ERROR_ARGUMENTS_INVALID

		with group.test("paste missing paths") as test:
			test.interactive([
				testbuild.InteractiveStep(
					input_line="paste",
					expect_stdout=lambda s: "ERROR" in s if "ERROR" in s else "ERROR in stdout"
				),
				testbuild.InteractiveStep(input_line="exit"),
			])
			test.returncode_policy = testbuild.ReturnCodePolicy.SHOULD_NOT_BE_ZERO
			test.returncode = __ERROR_ARGUMENTS_INVALID

		with group.test("empty input") as test:
			test.returncode_policy = testbuild.ReturnCodePolicy.SHOULD_BE_ZERO
			test.timeout = 2.0

	with tester.group("negative batch", categories = ["neg"]) as group:
		for f in ["neg_1.txt", "neg_2.txt", "neg_3.txt", "neg_4.txt",
			          "neg_5.txt", "neg_6.txt", "neg_7.txt", "neg_8.txt"]:
			input_path = os.path.join(__INPUT_DIR_ABS, f)
			if not os.path.exists(input_path):
				continue
			output_path = f.replace(".txt", "_out.txt")
			with group.test(f"batch {f}", seed_directory = __BATCH_SEED_ABS) as test:
				test.args = ["--input", input_path, "--output", output_path]
				test.returncode_policy = testbuild.ReturnCodePolicy.SHOULD_NOT_BE_ZERO
				test.stderr_policy = testbuild.StderrPolicy.NONEMPTY
				test.timeout = 5.0

	return tester

def __main() -> int:
	argument_parser = Utils.get_argument_parser()
	args = argument_parser.parse_args()

	tester = __get_tester()
	report = tester.run(args.program, timeout_factor = args.timeout_factor)

	results_path = args.github_actions_export_only_score_to
	if results_path and len(report.coefficients) != 0:
		with open(results_path, mode = "w", encoding = "UTF-8") as file:
			file.write(f"{report.score}\n")

	return report.exit_code

if __name__ == "__main__":
	sys.exit(__main())
