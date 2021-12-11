from pathlib import Path
from typing import Dict, Tuple

from .rusty_log_parser import parse_rust as _parse_rust


def parse_rust(input_file: Path) -> Dict[str, Tuple[int, int]]:
    """
    Parse log file using Rust as a backend.

    :param input_file: log file to parse.
    :return: Parsed
    """
    return _parse_rust(str(input_file.expanduser()))
