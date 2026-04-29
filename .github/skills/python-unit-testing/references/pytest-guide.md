# pytest Configuration Guide

## Installation

```bash
python -m pip install pytest pytest-cov pytest-mock pytest-asyncio
```

## Usage

```bash
# Run all tests
python -m pytest source/lib_test/

# Run specific file
python -m pytest source/lib_test/test_main.py

# Run with verbose output
python -m pytest source/lib_test/ -v

# Run specific test
python -m pytest source/lib_test/test_main.py::TestClass::test_method

# Run with coverage
python -m pytest source/lib_test/ --cov=source/lib --cov-report=html

# Run only fast tests (exclude slow)
python -m pytest source/lib_test/ -m "not slow"

# Run with markers
python -m pytest source/lib_test/ -m "unit"
```

## Configuration (pytest.ini)

Key options:
- `testpaths`: Where to look for tests
- `python_files`: Test file naming pattern
- `python_classes`: Test class naming pattern
- `python_functions`: Test function naming pattern
- `markers`: Custom markers for categorizing tests

## Pytest Plugins

- `pytest-cov`: Measure code coverage
- `pytest-mock`: Built-in mocking support
- `pytest-asyncio`: Async test support
- `pytest-timeout`: Timeout long-running tests

## Common Pytest Options

| Option | Purpose |
|--------|---------|
| `-v` | Verbose output |
| `-s` | Show print statements |
| `-x` | Stop on first failure |
| `-k <expr>` | Run tests matching expression |
| `-m <marker>` | Run tests with marker |
| `--lf` | Run last failed |
| `--ff` | Run failed then pass |
| `--co` | List tests without running |
