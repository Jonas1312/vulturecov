import abc
import json
from pathlib import Path

from .vulture_report import VultureReportLine


class AbstractCoverageReport(abc.ABC):
    @abc.abstractmethod
    def is_line_in_cov_report(self, line: VultureReportLine) -> bool:
        """Check if Vulture report line is in coverage report."""


class CoverageReportJson(AbstractCoverageReport):
    def __init__(self, cov_report_path: Path):
        assert (
            cov_report_path.suffix == ".json"
        ), f"Coverage report must be a json file: {cov_report_path}"

        self.cov_report = json.loads(cov_report_path.read_text())

    def is_line_in_cov_report(self, line: VultureReportLine) -> bool:
        """Check if Vulture report line is in coverage report."""
        file_path_str_windows = line.src_filepath.replace("/", "\\")
        filepath_str_posix = line.src_filepath.replace("\\", "/")

        if file_path_str_windows in self.cov_report["files"]:
            return (
                line.line_number
                in self.cov_report["files"][file_path_str_windows]["executed_lines"]
            )

        if filepath_str_posix in self.cov_report["files"]:
            return (
                line.line_number in self.cov_report["files"][filepath_str_posix]["executed_lines"]
            )

        return False
