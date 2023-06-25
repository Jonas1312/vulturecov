# [vulturecov](https://github.com/Jonas1312/vulturecov)

[![image](https://img.shields.io/pypi/v/vulturecov.svg)](https://pypi.python.org/pypi/vulturecov)
[![image](https://img.shields.io/pypi/pyversions/vulturecov.svg)](https://pypi.python.org/pypi/vulturecov)
[![Actions status](https://github.com/Jonas1312/vulturecov/workflows/CI/badge.svg)](https://github.com/Jonas1312/vulturecov/actions)

[**vulturecov**](https://github.com/Jonas1312/vulturecov) is a tool to filter the dead code false positives found by [Vulture](https://github.com/jendrikseipp/vulture) using [Coverage.py](https://coverage.readthedocs.io/e).

The rationale is that if a line of code is covered by a test, then it is unlikely to be dead code.

## Installation

```bash
pip install vulturecov
```

## Usage

First, generate the Vulture report:

```bash
vulture src/my_package > vulture_report.txt
vulture src/my_package whitelist.py > vulture_report.txt  # with a whitelist
```

Then, generate the Coverage report using pytest for example:

```bash
pytest --cov=src/my_package --cov-report=json:coverage.json
```

Once you have the two reports, you can use **vulturecov** to filter the Vulture report:

Show the dead code (lines of code that are found by Vulture and not covered by tests):

```bash
vulturecov vulture_report.txt coverage.json  # print the result to stdout
vulturecov vulture_report.txt coverage.json --output vulturecov_report.txt  # write the result to a file
```

Only show the false positives (lines of code that are covered by tests):

```bash
vulturecov vulture_report.txt coverage.json --false-positives  # print the result to stdout
vulturecov vulture_report.txt coverage.json --false-positives --output vulture_fp.txt  # write the result to a file
```

To add the false positives in your Vulture whitelist:

```bash
vulturecov vulture_report.txt coverage.json --false-positives >> whitelist.py
```
