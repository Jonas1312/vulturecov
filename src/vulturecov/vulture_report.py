import re
from dataclasses import dataclass
from pathlib import Path
from typing import Generator, Type


@dataclass
class VultureReportLine:
    src_filepath: str
    line_number: int
    raw_line: str

    @classmethod
    def from_str(cls: Type["VultureReportLine"], line: str) -> "VultureReportLine":
        REGEX = r"^(?:.*?\()?(.+?):(\d+).*"
        match = re.search(REGEX, line)
        assert match, f"Could not parse vulture line: {line}"

        path = match.group(1)
        line_number = int(match.group(2))
        return cls(raw_line=line, src_filepath=path, line_number=line_number)


def read_vulture(path: Path) -> Generator[str, None, None]:
    """Read vulture report line by line."""
    with Path(path).open("r", encoding="utf-8") as f:
        yield from f


def parse_and_read_vulture(path: Path) -> Generator[VultureReportLine, None, None]:
    """Parse vulture report line by line."""
    yield from (VultureReportLine.from_str(line) for line in read_vulture(path))
