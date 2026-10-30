import argparse
import os

from pathlib import Path
from typing import Mapping, Optional

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

	parser.add_argument(
		"--github-actions-export-only-score-to",
		required = False,
		type = Path,
		help = "export only final score from a test results report to file"
	)

	return parser

def get_coefficients(target_name: str, cat_to_env_mapper: Mapping[str, str]) -> Optional[Mapping[str, float]]:
	coefficents: Dict[str, float] = {}

	for category, env in cat_to_env_mapper.items():
		key = f"SE_C26_{target_name.upper()}_{env}"
		value = os.getenv(key)

		if value is None:
			return None

		try:
			coefficient = float(value)
			coefficents[category] = coefficient
		except Exception as _:
			return None

	return coefficents
