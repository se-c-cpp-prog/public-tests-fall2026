#!/usr/bin/env python3

import sys
import os
import numpy as np

import testbuild

import Utils

from typing import Union, Iterable, List, Dict, Any
from dataclasses import dataclass

__TARGET_NAME = "Math"
__SEED = 123456
__CATEGORIES_TO_ENVIROMENT_MAPPER = {
	"det": "DET",
	"mul": "MUL",
	"pow": "POW",
	"sub": "SUB",
	"sum": "SUM",
	"neg": "NEG"
}

__BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "testdata", "math")
__INPUT_DIR = os.path.join(__BASE_DIR, "input")
__OUTPUT_DIR = os.path.join(__BASE_DIR, "output")
__REFERENCE_DIR = os.path.join(__BASE_DIR, "reference")

__ERROR_SUCCESS = 0
__ERROR_CANNOT_OPEN_FILE = 1
__ERROR_OUT_OF_MEMORY = 2
__ERROR_DATA_INVALID = 3
__ERROR_ARGUMENTS_INVALID = 4

@dataclass
class TestData:
	name: str
	input_filename: str
	output_filename: str
	reference_filename: str
	returncode_policy: testbuild.ReturnCodePolicy
	returncode: int
	timeout: float

@dataclass
class NegTestData:
	name: str
	args: List[str]
	returncode: int
	timeout: float

class __Expected(testbuild.Expected):
	def __init__(self, testdata: TestData) -> None:
		super().__init__()
		self.__testdata = testdata
		self.__delta = 1e-4

	def test(self, run: testbuild.Run, runned: testbuild.Runned) -> testbuild.Verdict:
		def __generate_mtx_from_lists(nested_list: List[List[str]]) -> Union[np.ndarray, testbuild.Verdict]:
			matrix = np.zeros(shape = (len(nested_list), len(nested_list[0])), dtype = np.float32)
			for y in range(matrix.shape[0]):
				for x in range(matrix.shape[1]):
					try:
						matrix[y][x] = np.float32(nested_list[y][x])
					except Exception:
						if (nested_list[y][x] == "-nan(ind)"):
							matrix[y][x] = np.float32(np.nan)
						else:
							return testbuild.Verdict(
								testbuild.VerdictCode.EXPECTATION,
								f"expected float value at position ({y}, {x}), but found '{nested_list[y][x]}'"
							)
			return matrix

		# Extract output filename.
		output_filename = self.__testdata.output_filename

		# Extract reference filename.
		reference_filename = self.__testdata.reference_filename

		# Check output file existing.
		if not os.path.exists(output_filename):
			return testbuild.Verdict(
				testbuild.VerdictCode.EXPECTATION,
				f"file not found: {output_filename}"
			)

		# Read files.
		actual = [s.strip() for s in open(output_filename, "r").readlines()]
		expected = [s.strip() for s in open(reference_filename, "r").readlines()]

		# Check number of lines.
		if len(actual) != len(expected):
			return testbuild.Verdict(
				testbuild.VerdictCode.EXPECTATION,
				f"wrong number of lines: {len(actual)} (in '{output_filename}') vs. {len(expected)} (in '{reference_filename}')"
			)

		# Check on 'no solution'.
		if expected[0] == "no solution":
			if actual[0] != "no solution":
				return testbuild.Verdict(
					testbuild.VerdictCode.EXPECTATION,
					f"expected 'no solution' as answer, but found something else"
				)

			return testbuild.OK

		# Check on 'det' operation.
		if len(expected) == 1:
			det_ref = np.abs(np.float32(expected[0]))

			try:
				det_out = np.abs(np.float32(actual[0]))

				if np.isnan(det_ref) and not np.isnan(det_out) or not np.isnan(det_ref) and np.isnan(det_out) or np.abs(det_ref - det_out) / np.fmax(det_ref, det_out) > self.__delta:
					return testbuild.Verdict(
						testbuild.VerdictCode.EXPECTATION,
						f"wrong det-operation answer, found {det_out}, expected {det_ref} with relative delta {self.__delta}"
					)

				return testbuild.OK
			except Exception:
				return testbuild.Verdict(
					testbuild.VerdictCode.EXPECTATION,
					f"expected float value as det-operation answer, but found '{actual[0]}'"
				)

		# Expect sizes.
		sizes_ref = list(map(int, expected[0].split(" ")))
		sizes_out: List[int] = []
		try:
			sizes_out = list(map(int, actual[0].split(" ")))
		except Exception:
			return testbuild.Verdict(
				testbuild.VerdictCode.EXPECTATION,
				f"expected matrix sizes, but found '{actual[0]}'"
			)

		if sizes_ref[0] != sizes_out[0] or sizes_ref[1] != sizes_out[1]:
			return testbuild.Verdict(
				testbuild.VerdictCode.EXPECTATION,
				f"wrong matrix sizes, expected {sizes_ref[0]}x{sizes_ref[1]}, but found {sizes_out[0]}x{sizes_out[1]}"
			)

		# Comparison matrices.
		nested_actual_matrix = [s.strip().split(' ') for s in actual[1:]]
		nested_expected_matrix = [s.strip().split(' ') for s in expected[1:]]
		
		if len(nested_actual_matrix) != len(nested_expected_matrix) or len(nested_actual_matrix[0]) != len(nested_expected_matrix[0]):
			return testbuild.Verdict(
				testbuild.VerdictCode.EXPECTATION,
				f"Matrix size mismatch: expected {len(nested_expected_matrix)}x{len(nested_expected_matrix[0])}, but got {len(nested_actual_matrix)}x{len(nested_actual_matrix[0])}"
			)

		generate_mtx_result = __generate_mtx_from_lists(nested_actual_matrix)
		if isinstance(generate_mtx_result, testbuild.Verdict):
			return generate_mtx_result
		actual_matrix = generate_mtx_result

		generate_mtx_result = __generate_mtx_from_lists(nested_expected_matrix)
		if isinstance(generate_mtx_result, testbuild.Verdict):
			return generate_mtx_result
		expected_matrix = generate_mtx_result

		max_abs = np.fmax(np.abs(expected_matrix), np.abs(actual_matrix))
		max_by_row = np.amax(max_abs, axis = 1)
		max_by_col = np.amax(max_abs, axis = 0)

		for y in range(expected_matrix.shape[0]):
			for x in range(expected_matrix.shape[1]):
				a = actual_matrix[y][x]
				e = expected_matrix[y][x]

				if np.isnan(a) and np.isnan(e):
					continue
				if np.isnan(a) and not np.isnan(e) or not np.isnan(a) and np.isnan(e):
					return testbuild.Verdict(
						testbuild.VerdictCode.EXPECTATION,
						f"at (row, column)=({y}, {x}) position should be '{str(e)}', but actual is '{str(a)}'"
					)
				
				diff = abs(a - e)
				m = min(max_by_row[y], max_by_col[x])
				d = diff / m
				if d > self.__delta:
					return testbuild.Verdict(
						testbuild.VerdictCode.EXPECTATION,
						f"at (row, column)=({y}, {x}) position should be '{str(e)}', but actual is '{str(a)}'"
					)

		return testbuild.OK

def __generate_test(test_data: dict) -> Union[np.ndarray, np.float32, str]:
	op = test_data["op"]
	amtx = test_data["amtx"]
	
	if (op in {"+", "-", "*"}):
		bmtx = test_data["bmtx"]
	elif (op == "^"):
		p = test_data["p"]

	try:
		if (op == "+"):
			if (amtx.shape != bmtx.shape):
				raise np.linalg.LinAlgError
			return amtx + bmtx
		elif (op == "-"):
			if (amtx.shape != bmtx.shape):
				raise np.linalg.LinAlgError
			return amtx - bmtx
		elif (op == "*"):
			return np.linalg.matmul(amtx, bmtx)
		elif (op == "^"):
			return np.linalg.matrix_power(amtx, p)
		else:
			return np.float32(np.linalg.det(amtx))
	except:
		return "no solution"

def __get_tests(category_name: str, neg: bool) -> Iterable[TestData]:
	tests: Iterable[TestData] = []

	def __f(x: str) -> bool:
		return category_name in x and ("neg" in x if neg else not "neg" in x)

	ts = list(filter(__f, os.listdir(__INPUT_DIR)))

	for i, t in enumerate(ts):
		input_filename = os.path.join(__INPUT_DIR, t)
		name = f"{category_name} #{i + 1} (see: {os.path.relpath(input_filename)})"
		output_filename = os.path.join(__OUTPUT_DIR, t)
		reference_filename = os.path.join(__REFERENCE_DIR, t)
		returncode_policy = testbuild.ReturnCodePolicy.MATCH_IF_PRESENTED if neg else testbuild.ReturnCodePolicy.SHOULD_BE_ZERO
		returncode = __ERROR_DATA_INVALID if neg else __ERROR_SUCCESS
		tests.append(TestData(
			name, input_filename, output_filename, reference_filename, returncode_policy, returncode, 1.0
		))

	return tests

def __print_mtx_to_file(file, mtx):
	rc = mtx.shape
	file.write(f"{rc[0]} {rc[1]}\n")
	for i in range(0, rc[0]):
		for k in range(0, rc[1]):
			file.write("{:g} ".format(mtx[i][k]))
		file.write("\n")

def __generate_rnd_mtx(rng, sizes, multiply):
	return rng.random(size = sizes, dtype = np.float32) * multiply

def __get_big_tests(category_name: str, rng: np.random.Generator, test_params: Dict[str, Any]) -> Iterable[TestData]:
	tests: List[TestData] = []

	SUFFIX = "big"
	POW_CONSTANT = 8
	TIMEOUT_CONSTANT = 4.0 if (test_params["op"] == "*" or test_params["op"] == "|" or test_params["op"] == "^") else 1.0

	for i, param in enumerate(test_params["params"]):
		__make_filename = f"{SUFFIX}_{category_name}_{param['suffix']}.txt"
		make_test_input_filename = os.path.join(__INPUT_DIR, __make_filename)

		test_name = f"Big {category_name} #{i + 1} (see: {os.path.relpath(make_test_input_filename)})"
		test_input_filename = make_test_input_filename
		test_output_filename = os.path.join(__OUTPUT_DIR, __make_filename)
		test_reference_filename = os.path.join(__REFERENCE_DIR, __make_filename)

		size = param['size']
		amtx = (np.zeros(shape=size, dtype=np.float32) if (param['type'] == "zeros") else np.eye(N=size[0], dtype=np.float32) if(param['type'] == "eye") else __generate_rnd_mtx(rng, sizes=size, multiply=1.0))
		bmtx = (np.zeros(shape=size, dtype=np.float32) if (param['type'] == "zeros") else np.eye(N=size[0], dtype=np.float32) if(param['type'] == "eye") else __generate_rnd_mtx(rng, sizes=size, multiply=1.0))
		op = test_params["op"]


		stream_input = open(test_input_filename, "w")
		stream_input.write(f"{op}\n")
		__print_mtx_to_file(stream_input, amtx)
		if category_name == "pow":
			stream_input.write(f"{POW_CONSTANT}\n")
		elif category_name != "det":
			__print_mtx_to_file(stream_input, bmtx)
		stream_input.close()

		result = None
		if category_name == "det":
			result = __generate_test({ "op": op, "amtx": amtx })
		elif category_name == "pow":
			result = __generate_test({ "op": op, "amtx": amtx, "p": POW_CONSTANT })
		else:
			result = __generate_test({ "op": op, "amtx": amtx, "bmtx": bmtx })

		stream_reference = open(test_reference_filename, "w")
		if isinstance(result, str) and result == "no solution":
			stream_reference.write("no solution\n")
		elif isinstance(result, np.float32):
			stream_reference.write(f"{result:g}\n")
		else:
			__print_mtx_to_file(stream_reference, result)

		stream_reference.close()

		tests.append(TestData(
			test_name,
			test_input_filename, test_output_filename,
			test_reference_filename,
			testbuild.ReturnCodePolicy.SHOULD_BE_ZERO, 0,
			TIMEOUT_CONSTANT
		))

	return tests

def __get_additional_negative_tests() -> List[NegTestData]:
	tests: List[NegTestData] = []

	input_filename = os.path.join(__INPUT_DIR, f"random_name.txt")
	output_filename = os.path.join(__OUTPUT_DIR, f"random_name.txt")
	tests.append(NegTestData(
		f"no input file",
		[input_filename, output_filename],
		__ERROR_CANNOT_OPEN_FILE, 1.0
	))

	input_filename = os.path.join(__INPUT_DIR, "sum_1.txt")
	output_filename = os.path.join(__OUTPUT_DIR, "non_existing_folder", f"random_name.txt")
	tests.append(NegTestData(
		f"can't write to output file",
		[input_filename, output_filename],
		__ERROR_CANNOT_OPEN_FILE, 1.0
	))

	input_filename = os.path.join(__INPUT_DIR, "oom_1.txt")
	output_filename = os.path.join(__OUTPUT_DIR, f"random_name.txt")
	tests.append(NegTestData(
		f"this should be out of memory error",
		[input_filename, output_filename],
		__ERROR_OUT_OF_MEMORY, 1.0
	))

	input_filename = os.path.join(__INPUT_DIR, "oom_2.txt")
	output_filename = os.path.join(__OUTPUT_DIR, f"random_name.txt")
	tests.append(NegTestData(
		f"this also should be out of memory error",
		[input_filename, output_filename],
		__ERROR_OUT_OF_MEMORY, 1.0
	))

	tests.append(NegTestData(
		f"only 1 argument provided",
		[input_filename],
		__ERROR_ARGUMENTS_INVALID, 1.0
	))

	tests.append(NegTestData(
		f"zero arguments provided",
		[],
		__ERROR_ARGUMENTS_INVALID, 1.0
	))

	tests.append(NegTestData(
		f"too much arguments provided",
		[input_filename, output_filename, input_filename],
		__ERROR_ARGUMENTS_INVALID, 1.0
	))

	return tests

def __get_tester() -> testbuild.Tester:
	tester = testbuild.Tester(__TARGET_NAME, coefficients = Utils.get_coefficients(__TARGET_NAME, __CATEGORIES_TO_ENVIROMENT_MAPPER))

	rng = np.random.default_rng(seed = __SEED)
	test_data = {
		"det": {
			"op": "|",
			"params": [
				{
					"type": "rnd",
					"suffix": "1_9",
					"size": (1000, 1000)
				},
				{
					"type": "zeros",
					"suffix": "8",
					"size": (1000, 1000)
				},
				{
					"type": "eye",
					"suffix": "9",
					"size": (1000, 1000)
				}
			]
		},
		"mul": {
			"op": "*",
			"params": [
				{
					"type": "rnd",
					"suffix": "6",
					"size": (1000, 1000)
				}
			]
		},
		"pow": {
			"op": "^",
			"params": [
				{
					"type": "rnd",
					"suffix": "16",
					"size": (500, 500)
				}
			]
		},
		"sub": {
			"op": "-",
			"params": [
				{
					"type": "rnd",
					"suffix": "5",
					"size": (1000, 1000)
				}
			]
		},
		"sum": {
			"op": "+",
			"params": [
				{
					"type": "rnd",
					"suffix": "6",
					"size": (1000, 1000)
				}
			]
		}
	}

	np.seterr(all = "ignore")

	for category_name in test_data.keys():
		tests = {
			"normal": __get_tests(category_name, False),
			"neg": __get_tests(category_name, True),
			"big": __get_big_tests(category_name, rng, test_data[category_name])
		}

		for name, testdatas in tests.items():
			group_categories = [category_name]

			# neg tests should be part of neg category.
			if name == "neg":
				group_categories = ["neg"]

			with tester.group(f"{name} {category_name}", categories = group_categories) as group:
				for testdata in testdatas:
					with group.test(testdata.name) as test:
						test.args = [testdata.input_filename, testdata.output_filename]
						test.returncode_policy = testdata.returncode_policy
						test.returncode = testdata.returncode
						test.timeout = testdata.timeout
						if test.returncode == __ERROR_SUCCESS:
							test.expected = __Expected(testdata)

	additional_neg_tests = __get_additional_negative_tests()
	with tester.group(f"additional negative tests", categories = ["neg"]) as group:
		for testdata in additional_neg_tests:
			with group.test(testdata.name) as test:
				test.args = testdata.args
				test.returncode = testdata.returncode
				test.timeout = testdata.timeout

	return tester

def __main() -> int:
	argument_parser = Utils.get_argument_parser()
	args = argument_parser.parse_args()

	print("Warning! This tester generates really big matrices. Have some patience...")

	tester = __get_tester()
	report = tester.run(args.program, timeout_factor = args.timeout_factor)

	results_path = args.github_actions_export_only_score_to
	if results_path and len(report.coefficients) != 0:
		with open(results_path, mode = "w", encoding = "UTF-8") as file:
			file.write(f"{report.score}\n")

	return report.exit_code

if __name__ == "__main__":
	sys.exit(__main())
