from pathlib import Path

import pytest
import pytest_mock
from click.testing import CliRunner

from vulturecov.__main__ import main


def test_cli_stdout():
    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            "tests/data/kili/vulture_normal_mode.txt",
            "tests/data/kili/be84cc6b9fd4a990fa9eaa0dd26de22aaa15f9ff.json",
        ],
    )
    assert result.exit_code == 0
    assert (
        result.output
        # ruff: noqa: E501
        == r"""src/kili/core/graphql/graphql_client.py:311: unused attribute 'on_message' (60% confidence)
src/kili/core/graphql/operations/lock/queries.py:8: unused class 'LockWhere' (60% confidence)
src/kili/core/graphql/operations/lock/queries.py:23: unused class 'LockQuery' (60% confidence)
src/kili/entrypoints/mutations/asset/__init__.py:168: unused variable 'priorities' (100% confidence)
src/kili/entrypoints/mutations/asset/__init__.py:169: unused variable 'json_metadatas' (100% confidence)
src/kili/entrypoints/mutations/asset/__init__.py:170: unused variable 'consensus_marks' (100% confidence)
src/kili/entrypoints/mutations/asset/__init__.py:171: unused variable 'honeypot_marks' (100% confidence)
src/kili/entrypoints/mutations/asset/__init__.py:172: unused variable 'to_be_labeled_by_array' (100% confidence)
src/kili/entrypoints/mutations/asset/__init__.py:174: unused variable 'json_contents' (100% confidence)
src/kili/entrypoints/mutations/asset/__init__.py:176: unused variable 'is_used_for_consensus_array' (100% confidence)
src/kili/entrypoints/mutations/data_connection/exceptions.py:4: unused class 'AddDataConnectionError' (60% confidence)
src/kili/entrypoints/queries/data_integration/queries.py:3: unused variable 'GQL_GET_DATA_INTEGRATION_FOLDER_AND_SUBFOLDERS' (60% confidence)
src/kili/services/plugins/model.py:40: unused method 'on_submit' (60% confidence)
src/kili/services/plugins/model.py:68: unused method 'on_review' (60% confidence)
src/kili/services/plugins/model.py:98: unused method 'on_custom_interface_click' (60% confidence)
"""
    )


@pytest.mark.parametrize(
    "vulture_report_filepath,output_contains",
    (
        (
            "tests/data/kili/vulture_normal_mode.txt",
            "src/kili/entrypoints/mutations/label/__init__.py:41: unused method 'create_predictions' (60% confidence)",
        ),
        (
            "tests/data/kili/vulture_make_whitelist_mode.txt",
            "_.create_predictions  # unused method (src/kili/entrypoints/mutations/label/__init__.py:41)",
        ),
    ),
)
def test_cli_stdout_print_false_positives(vulture_report_filepath: str, output_contains: str):
    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            vulture_report_filepath,
            "tests/data/kili/be84cc6b9fd4a990fa9eaa0dd26de22aaa15f9ff.json",
            "--false-positives",
        ],
    )
    assert result.exit_code == 0
    assert output_contains in result.output


def test_cli_stdout_exit_1():
    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            "tests/data/kili/vulture_normal_mode.txt",
            "tests/data/kili/be84cc6b9fd4a990fa9eaa0dd26de22aaa15f9ff.json",
            "-e",
        ],
    )
    assert result.exit_code != 0


def test_cli_to_file():
    output_file = "filtered.txt"
    Path(output_file).unlink(missing_ok=True)
    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            "tests/data/kili/vulture_normal_mode.txt",
            "tests/data/kili/be84cc6b9fd4a990fa9eaa0dd26de22aaa15f9ff.json",
            "-o",
            output_file,
        ],
    )
    assert result.exit_code == 0
    assert Path(output_file).exists()
    assert (
        Path(output_file).read_text(encoding="utf-8")
        # ruff: noqa: E501
        == r"""src/kili/core/graphql/graphql_client.py:311: unused attribute 'on_message' (60% confidence)
src/kili/core/graphql/operations/lock/queries.py:8: unused class 'LockWhere' (60% confidence)
src/kili/core/graphql/operations/lock/queries.py:23: unused class 'LockQuery' (60% confidence)
src/kili/entrypoints/mutations/asset/__init__.py:168: unused variable 'priorities' (100% confidence)
src/kili/entrypoints/mutations/asset/__init__.py:169: unused variable 'json_metadatas' (100% confidence)
src/kili/entrypoints/mutations/asset/__init__.py:170: unused variable 'consensus_marks' (100% confidence)
src/kili/entrypoints/mutations/asset/__init__.py:171: unused variable 'honeypot_marks' (100% confidence)
src/kili/entrypoints/mutations/asset/__init__.py:172: unused variable 'to_be_labeled_by_array' (100% confidence)
src/kili/entrypoints/mutations/asset/__init__.py:174: unused variable 'json_contents' (100% confidence)
src/kili/entrypoints/mutations/asset/__init__.py:176: unused variable 'is_used_for_consensus_array' (100% confidence)
src/kili/entrypoints/mutations/data_connection/exceptions.py:4: unused class 'AddDataConnectionError' (60% confidence)
src/kili/entrypoints/queries/data_integration/queries.py:3: unused variable 'GQL_GET_DATA_INTEGRATION_FOLDER_AND_SUBFOLDERS' (60% confidence)
src/kili/services/plugins/model.py:40: unused method 'on_submit' (60% confidence)
src/kili/services/plugins/model.py:68: unused method 'on_review' (60% confidence)
src/kili/services/plugins/model.py:98: unused method 'on_custom_interface_click' (60% confidence)
"""
    )
    Path(output_file).unlink(missing_ok=True)


def test_cli_no_dead_code(mocker: pytest_mock.MockFixture):
    mocker.patch("vulturecov.__main__.filter_vulture_lines", return_value=[])
    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            "tests/data/kili/vulture_normal_mode.txt",
            "tests/data/kili/be84cc6b9fd4a990fa9eaa0dd26de22aaa15f9ff.json",
        ],
    )
    assert result.exit_code == 0
    assert "Nothing to output." in result.output
