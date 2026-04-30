# Test Coverage Best Practices

## Understanding Coverage

Code coverage measures what percentage of code is executed by tests.

```
Coverage = (Lines executed by tests) / (Total lines) * 100%
```

## Coverage Metrics

```bash
# Generate coverage report
python -m pytest source/lib_test/ --cov=source/lib --cov-report=term-missing

# HTML report (open htmlcov/index.html)
python -m pytest source/lib_test/ --cov=source/lib --cov-report=html

# Branch coverage (if statements, etc.)
python -m pytest source/lib_test/ --cov=source/lib --cov-branch
```

## Coverage Targets

- **Minimum**: 50% (better than nothing)
- **Good**: 70-80% (reasonable coverage)
- **Excellent**: 85-95% (high quality)
- **100%**: Possible but not always valuable

## Don't Chase 100%

Some code shouldn't be tested:
- Generated code
- Database migrations
- CLI error messages
- Third-party integrations (mock instead)

```python
# Skip from coverage measurement
import sys
import pytest

# Option 1: Pragma comment
def risky_feature():  # pragma: no cover
    raise SystemExit()

# Option 2: Skip in pytest
@pytest.mark.skipif(sys.version_info < (3, 10), reason="requires py3.10")
def test_new_feature():
    pass
```

## Coverage-Guided Testing

```python
# Coverage report shows: line 15 not covered
def process_payment(user, amount):
    if amount <= 0:  # Line 15 - UNCOVERED
        raise ValueError("Amount must be positive")
    return user.debit(amount)

# Add test for missing case
def test_process_payment_negative_amount():
    with pytest.raises(ValueError):
        process_payment(user, -10)
```

## Tools

- **pytest-cov**: Measure coverage during pytest
- **Coverage.py**: Detailed coverage reports
- **Codecov**: CI/CD coverage tracking

## Configuration (.coveragerc)

```ini
[run]
source = source/lib
omit =
    */tests/*
    */site-packages/*

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise NotImplementedError
```
