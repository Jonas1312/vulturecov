from pathlib import Path

import pytest

from vulturecov.cov_report import CoverageReportJson
from vulturecov.vulture_report import VultureReportLine


@pytest.mark.parametrize(
    "src_filepath,line_number",
    (
        ("src/kili/__init__.py", 4),
        ("src/kili/entrypoints/mutations/asset/__init__.py", 49),
    ),
)
def test_is_line_in_cov_report_json(src_filepath: str, line_number: int) -> None:
    test_coverate_report_json = Path(
        "tests/data/kili/be84cc6b9fd4a990fa9eaa0dd26de22aaa15f9ff.json"
    )
    cov_report = CoverageReportJson(test_coverate_report_json)

    line = VultureReportLine(raw_line="", src_filepath=src_filepath, line_number=line_number)
    assert cov_report.is_line_in_cov_report(line)
