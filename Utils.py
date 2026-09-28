import argparse

from pathlib import Path

def get_argument_parser() -> argparse.ArgumentParser:
	parser = argparse.ArgumentParser()

	parser.add_argument(
		"--program", "-p",
		required = True,
		type = Path,
		help = "path to the executable file to be tested"
	)

	parser.add_argument(
		"--timeout-factor", "-t",
		required = False,
		type = float, default = 1.0,
		help = "maximum program execution time multiplier (default: 1.0)"
	)

	return parser
