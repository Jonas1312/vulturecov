import pytest

from vulturecov.vulture_report import VultureReportLine


@pytest.mark.parametrize(
    "line, filepath, line_number",
    (
        (
            "_.internal  # unused attribute (src/kili/client.py:137)",
            "src/kili/client.py",
            137,
        ),
        (
            r"_.internal  # unused attribute (src\kili\client.py:137)",
            r"src\kili\client.py",
            137,
        ),
        (
            r"src\vulturecov\cov_report.py:41: unused variable 'a' (60% confidence)",
            r"src\vulturecov\cov_report.py",
            41,
        ),
        (
            "src/kili/client.py:137: unused attribute 'internal' (60% confidence)",
            "src/kili/client.py",
            137,
        ),
        (
            "src/kili/core/enums.py:11: unused variable 'DataIntegrationType' (60% confidence)",
            "src/kili/core/enums.py",
            11,
        ),
        (
            "src/kili/entrypoints/mutations/organization/__init__.py:29: unused method 'create_organization' (60% confidence)",  # noqa: E501
            "src/kili/entrypoints/mutations/organization/__init__.py",
            29,
        ),
        (
            "src/kili/types.py:60: unused variable 'numberOfAnnotations' (60% confidence)",
            "src/kili/types.py",
            60,
        ),
        (
            "src/kili/utils/labels/image.py:27: unused function 'mask_to_normalized_vertices' (60% confidence)",  # noqa: E501
            "src/kili/utils/labels/image.py",
            27,
        ),
        (
            "LockWhere  # unused class (src/kili/core/graphql/operations/lock/queries.py:8)",
            "src/kili/core/graphql/operations/lock/queries.py",
            8,
        ),
        (
            "GQL_GET_DATA_INTEGRATION_FOLDER_AND_SUBFOLDERS  # unused variable (src/kili/entrypoints/queries/data_integration/queries.py:3)",  # noqa: E501
            "src/kili/entrypoints/queries/data_integration/queries.py",
            3,
        ),
        (
            "inputType  # unused variable (src/kili/services/label_data_parsing/types.py:14)",
            "src/kili/services/label_data_parsing/types.py",
            14,
        ),
        (
            "createdAt  # unused variable (src/kili/types.py:282)",
            "src/kili/types.py",
            282,
        ),
        (
            "mask_to_normalized_vertices  # unused function (src/kili/utils/labels/image.py:27)",
            "src/kili/utils/labels/image.py",
            27,
        ),
    ),
)
def test_parse_vulture_line(line: str, filepath: str, line_number: int) -> None:
    parsed_line = VultureReportLine.from_str(line)
    assert parsed_line.raw_line == line
    assert parsed_line.src_filepath == filepath
    assert parsed_line.line_number == line_number
