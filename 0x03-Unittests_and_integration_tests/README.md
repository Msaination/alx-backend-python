# GitHub Org Client Utilities

This repository provides reusable Python utilities and tests for working with nested mappings, remote JSON data, and memoization. All code is fully documented, type-annotated, executable, and compliant with [pycodestyle 2.5](https://pycodestyle.readthedocs.io/en/latest/).

## 📦 Contents

- `utils.py` — Core utility functions:
  - `access_nested_map`: Safely access values in nested dictionaries.
  - `get_json`: Fetch and parse JSON from a remote URL.
  - `memoize`: Decorator to cache method results.

- `test_utils.py` — Unit tests for `access_nested_map` using `unittest` and `parameterized`.

## ✅ Standards

All modules, classes, and functions follow these conventions:

- ✅ Module-level docstrings (visible via `python3 -c 'print(__import__("module").__doc__)'`)
- ✅ Class and function docstrings
- ✅ Type annotations for all functions and coroutines
- ✅ Executable scripts (`if __name__ == "__main__":`)
- ✅ pycodestyle 2.5 compliance

## 🧪 Running Tests

To run the test suite:

```bash
python3 test_utils.py
