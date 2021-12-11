import secrets
import time
import uuid
from pathlib import Path
from typing import Any

import typer

from python_rust.py_parser import parse_python
from rusty_log_parser import parse_rust

tpr = typer.Typer()


def quote(somthing: Any) -> str:
    """
    Quote string.

    :param somthing: any string.
    :return: quoted string.
    """
    return f'"{somthing}"'


@tpr.command()
def generator(  # noqa: WPS210
    output: Path,
    lines: int = 2_000_000,  # noqa: WPS303
    ids: int = 1000,
) -> None:
    """
    Test log generator.

    :param ids: how many file id's to generate.
    :param output: output file path.
    :param lines: how many lines to write, defaults to 2_000_000
    """
    ids_pool = [uuid.uuid4().hex for _ in range(ids)]

    with open(output, "w") as out_file:
        for line_num in range(lines):
            item_id = secrets.choice(ids_pool)
            prefix = secrets.token_hex(60)
            url = f"GET /{prefix}/{item_id}.jpg"
            current_time = int(time.time())
            bytes_sent = secrets.randbelow(800)  # noqa: WPS432
            line = [
                quote(line_num),
                quote("-"),
                quote(url),
                quote(current_time),
                quote(bytes_sent),
            ]
            out_file.write(" ".join(line))
            out_file.write("\n")
    typer.secho("Log successfully generated.", fg=typer.colors.GREEN)


@tpr.command()
def parser(input_file: Path, rust: bool = False) -> None:
    """
    Parse given log file.

    :param input_file: path of input file.
    :param rust: use rust parser implementation.
    """
    if rust:
        parsed_data = parse_rust(input_file)
    else:
        parsed_data = parse_python(input_file)

    typer.secho(
        f"Found {len(parsed_data)} files",  # noqa: WPS237
        color=typer.colors.CYAN,
    )


def main() -> None:
    """Main program entrypoint."""
    tpr()
