# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.


## Project Overview

**bitmath** is a pure-Python library (no external runtime dependencies) for representing and converting file sizes across SI (decimal) and NIST (binary) unit systems. It supports arithmetic (including floor division, modulo, and `divmod` for capacity math), rich comparisons, bitwise ops, parsing, formatting, and f-string/format() support.

## Project Direction
bitmath has been around for almost 12 years, and over that lifetime it promised to deliver backwards compatibility. It delivered on that promise and gathered a strong supporting of people and eventual "critical infrastructure" project status on the PyPI.org website.

As of January 2023 the project maintainer (me) has stated in this issue https://github.com/timlnx/bitmath/issues/99 that the project is still alive and the next release will be python 3 support only.

Much of that porting work has already happened in the `2023-01-26-no-more-py2` branch https://github.com/timlnx/bitmath/tree/2023-01-26-no-more-py2

### Current State (as of 2.0.0)

Phases 1 (maintenance 1.4.0) and 2 (bitmath 2.0.0) are complete. The project:

- Supports **Python 3.9 and newer only** (`requires-python = ">=3.9"` in `pyproject.toml`)
- Uses `hatchling` as the build backend (replaces `setup.py`)
- Uses `pytest` as the test runner (303 tests). Coverage is high but platform-sensitive: the `query_device_capacity` branches for the *other* OS are naturally uncovered on any single run.
- Is published on PyPI as version 2.0.0
- Drop-in compatible with the 1.x public API

## Common Commands

```bash
# Run the full test suite with coverage (creates venv, runs pytest + linting)
make ci

# Run linting only
ruff check bitmath/ tests/

# Build a wheel
make build

# Install in development mode
pip install -e .
```

Run a single test file:
```bash
python -m pytest tests/test_arithmetic.py -v
```

## Architecture

Almost all logic lives in a single file: `bitmath/__init__.py` (~1650 lines).

**Class hierarchy:**
- `Bitmath` — base class with all arithmetic, comparison, bitwise, formatting, and conversion logic
  - `Byte` — byte-based units; subclasses: `KiB MiB GiB TiB PiB EiB` (NIST/base-2) and `kB MB GB TB PB EB ZB YB` (SI/base-10)
  - `Bit` — bit-based units; subclasses: `Kib Mib Gib Tib Pib Eib` (NIST) and `kb Mb Gb Tb Pb Eb Zb Yb` (SI)

All unit values are normalized to bits internally; conversion between units happens at construction time via `_norm_value` and class-level `_base_value` / `_unit_value` constants.

**Key module-level functions:**
- `best_prefix(value, system=NIST)` — pick the most human-readable unit for a raw byte value
- `getsize(path, ...)` — file size with automatic prefix selection
- `listdir(search_base, ...)` — recursive directory listing with sizes
- `parse_string(s)` / `parse_string_unsafe(s, system=SI)` — string → bitmath object
- `query_device_capacity(device_fd)` — block device capacity on Linux (POSIX/`fcntl`) and Windows (`DeviceIoControl`); raises `NotImplementedError` on unsupported platforms (macOS lacks a usable ioctl under SIP)

**Constants:** `NIST`, `SI`, `NIST_PREFIXES`, `SI_PREFIXES`, `ALL_UNIT_TYPES`

## Testing Notes

- Test runner: `pytest`
- All tests are in `tests/` as `test_*.py` files
- Test case names must be unique across the suite — enforced by `tests/test_unique_testcase_names.sh`
- Coverage is platform-sensitive: Windows and POSIX `query_device_capacity` paths only run on their respective OS
- `unittest.mock` (stdlib) is used for patching in integration tests
