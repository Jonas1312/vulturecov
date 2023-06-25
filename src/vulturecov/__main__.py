import sys
from pathlib import Path
from typing import Generator, Iterable

import click

from .cov_report import AbstractCoverageReport, CoverageReportJson
from .vulture_report import VultureReportLine, parse_and_read_vulture


def filter_vulture_lines(
    lines: Iterable[VultureReportLine], cov_report: AbstractCoverageReport
) -> Generator[VultureReportLine, None, None]:
    """Filter vulture report lines."""
    return (line for line in lines if not cov_report.is_line_in_cov_report(line))


@click.command()
@click.argument(
    "vulture-report", type=click.Path(exists=True, dir_okay=False, path_type=Path, readable=True)
)
@click.argument(
    "cov-report", type=click.Path(exists=True, dir_okay=False, path_type=Path, readable=True)
)
@click.option(
    "--output",
    "-o",
    type=click.Path(dir_okay=False, path_type=Path),
    help="Output file path.",
    default=None,
)
@click.option(
    "--exit-1",
    "-e",
    is_flag=True,
    help="Exit 1 when dead code is detected.",
    default=False,
)
@click.version_option()
def main(
    cov_report: Path,
    vulture_report: Path,
    output: Path | None = None,
    exit_1: bool = False,
) -> None:
    """Filter vulture report file."""
    if not vulture_report.exists():
        raise FileNotFoundError(f"Could not find vulture report: {vulture_report}")

    if not cov_report.exists():
        raise FileNotFoundError(f"Could not find coverage report: {cov_report}")

    if not cov_report.suffix == ".json":
        raise ValueError(f"Coverage report must be a json file: {cov_report}")

    vulture_lines_gen = parse_and_read_vulture(vulture_report)

    filtered_lines = filter_vulture_lines(vulture_lines_gen, CoverageReportJson(cov_report))
    filtered_lines = list(filtered_lines)

    if not filtered_lines:
        return

    if output is None:
        for line in filtered_lines:
            print(line.raw_line, end="")

    else:
        with output.open("w", encoding="utf-8") as f:
            for line in filtered_lines:
                f.write(line.raw_line)

    if exit_1:
        sys.exit(1)


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
