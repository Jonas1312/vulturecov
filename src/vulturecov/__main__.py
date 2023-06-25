import sys
from pathlib import Path
from typing import Generator, Iterable, Union

import click

from .cov_report import AbstractCoverageReport, CoverageReportJson
from .vulture_report import VultureReportLine, parse_and_read_vulture


def filter_vulture_lines(
    lines: Iterable[VultureReportLine],
    cov_report: AbstractCoverageReport,
    remove_lines_in_cov_report: bool,
) -> Generator[VultureReportLine, None, None]:
    """Filter vulture report lines."""
    return (
        line
        for line in lines
        if remove_lines_in_cov_report is not cov_report.is_line_in_cov_report(line)
    )


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
@click.option(
    "--false-positives",
    is_flag=True,
    help="Only show false positives in output.",
    default=False,
)
@click.version_option()
def main(
    cov_report: Path,
    vulture_report: Path,
    output: Union[Path, None] = None,
    exit_1: bool = False,
    false_positives: bool = False,
) -> None:
    """Filter vulture report file."""
    assert vulture_report.exists(), f"Could not find vulture report: {vulture_report}"
    assert cov_report.exists(), f"Could not find coverage report: {cov_report}"
    assert cov_report.suffix == ".json", f"Coverage report must be a json file: {cov_report}"

    vulture_lines_gen = parse_and_read_vulture(vulture_report)

    filtered_lines = filter_vulture_lines(
        vulture_lines_gen,
        CoverageReportJson(cov_report),
        remove_lines_in_cov_report=not false_positives,
    )
    filtered_lines = list(filtered_lines)

    if not filtered_lines:
        print("Nothing to output.")
        return

    if output is None:
        for line in filtered_lines:
            print(line.raw_line, end="")

    else:
        with output.open("w", encoding="utf-8") as f:
            for line in filtered_lines:
                f.write(line.raw_line)

    if exit_1 and filtered_lines and not false_positives:
        sys.exit(1)
