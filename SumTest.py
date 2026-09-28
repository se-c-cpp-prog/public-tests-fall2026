#!/usr/bin/env python3

import sys

import testbuild

import Utils

class __Expected(testbuild.Expected):
	def __init__(self, a: int, b: int) -> None:
		self.a = a
		self.b = b

	def test(self, run: testbuild.Run, runned: testbuild.Runned) -> testbuild.Verdict:
		output = runned.get_stdout()
		if not output.endswith("\n"):
			return testbuild.Verdict(
				testbuild.VerdictCode.EXPECTATION,
				"newline at the end of stdout expected"
			)

		lines = output.splitlines()
		if len(lines) != 1:
			return testbuild.Verdict(
				testbuild.VerdictCode.EXPECTATION,
				f"one output line expected, got {len(lines)}"
			)

		line = lines[0]
		if line != line.strip():
			return testbuild.Verdict(
				testbuild.VerdictCode.EXPECTATION,
				"unexpected whitespace around the result"
			)

		try:
			actual = int(line)
		except ValueError:
			return testbuild.Verdict(
				testbuild.VerdictCode.EXPECTATION,
				f"an integer was expected, got {output!r}"
			)

		expected = self.a + self.b
		if actual != expected:
			return testbuild.Verdict(
				testbuild.VerdictCode.EXPECTATION,
				f"{self.a} + {self.b}: expected {expected}, got {actual}",
			)

		return testbuild.OK


def __get_tester() -> testbuild.Tester:
	tester = testbuild.Tester("Sum")

	with tester.group("valid input", categories = ["pos"]) as group:
		for a, b in [(1, 2), (-10, 4), (0, 0), (2_000_000_000, -1_000_000_000)]:
			with group.test(f"sum of {a} and {b}") as test:
				test.stdin = f"{a} {b}\n"
				test.expected = __Expected(a, b)

	with tester.group("invalid input", categories = ["neg"]) as group:
		for name, stdin in [
			("empty input", ""),
			("one integer", "42\n"),
			("not integers", "hello world\n"),
		]:
			with group.test(name) as test:
				test.stdin = stdin
				test.returncode = 1

	return tester


def __main() -> int:
	argument_parser = Utils.get_argument_parser()
	args = argument_parser.parse_args()
	tester = __get_tester()
	report = tester.run(args.program, timeout_factor = args.timeout_factor)
	return report.exit_code


if __name__ == "__main__":
	sys.exit(__main())
