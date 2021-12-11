import shlex
from pathlib import Path
from typing import Dict, Tuple


def parse_python(  # noqa: WPS210
    filename: Path,
) -> Dict[str, Tuple[int, int]]:
    """
    Parse log file with python.

    :param filename: log file.
    :return: parsed data.
    """
    parsed_data = {}
    with open(filename, "r") as input_file:
        for line in input_file:
            spl = shlex.split(line)
            # Splitting method and actual url.
            url = spl[2].split()[1]
            # Splitting url by /
            # This split will turn "/test/aaa.png"
            # into "aaa".
            file_id = url.split("/")[-1].split(".")[0]
            file_info = parsed_data.get(file_id)
            # If information about file isn't found.
            if file_info is None:
                downloads, bytes_sent = 0, 0
            else:
                downloads, bytes_sent = file_info
            # Incrementing counters.
            downloads += 1
            bytes_sent += int(spl[4])
            # Saving back.
            parsed_data[file_id] = (downloads, bytes_sent)
    return parsed_data
