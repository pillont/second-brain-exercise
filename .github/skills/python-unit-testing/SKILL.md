---
name: python-unit-testing
description: "Write and run unit tests for Python code using pytest or unittest. Use when: testing individual functions/methods, mocking dependencies, testing edge cases, arranging test fixtures, or validating test coverage."
argument-hint: "Optional: test file name or function to test"
---

# Python Unit Testing

## When to Use

- Test individual functions or methods in isolation
- Mock external dependencies (files, APIs, databases)
- Test both success and failure scenarios
- Verify edge cases (empty inputs, negative numbers, None values)
- Ensure high code coverage (>80% target)
- Build confidence before integration tests
- Catch regressions early

## Unit Testing Frameworks

### Pytest (Recommended)

```bash
python -m pip install pytest pytest-cov pytest-mock
python -m pytest source/tests/ -v --cov=source
```

### Unittest (Standard Library)

```python
import unittest

class TestCalculator(unittest.TestCase):
    def test_add(self):
        self.assertEqual(2 + 2, 4)

if __name__ == '__main__':
    unittest.main()
```

## pytest Pattern: Arrange-Act-Assert (AAA)

### 1. Basic Test Structure

```python
import pytest
from source.lib import Calculator

class TestCalculator:
    """Test suite for Calculator class."""

    def test_add_positive_numbers(self):
        # ARRANGE: Set up test data
        calc = Calculator()
        a, b = 2, 3

        # ACT: Execute function
        result = calc.add(a, b)

        # ASSERT: Verify result
        assert result == 5

    def test_divide_by_zero_raises_error(self):
        # ARRANGE
        calc = Calculator()

        # ACT & ASSERT: Verify exception is raised
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            calc.divide(10, 0)
```

### 2. Fixtures & Setup/Teardown

```python
import pytest
from unittest.mock import Mock

@pytest.fixture
def calculator():
    """Fixture: provide Calculator instance."""
    return Calculator()

@pytest.fixture
def mock_database():
    """Fixture: mock database connection."""
    return Mock()

class TestUserService:
    def test_create_user(self, calculator, mock_database):
        # Use fixtures
        user_service = UserService(mock_database)
        mock_database.save.return_value = True

        result = user_service.create_user("Alice")
        
        assert result is True
        mock_database.save.assert_called_once()
```

### 3. Parametrized Tests

```python
import pytest

@pytest.mark.parametrize("input,expected", [
    (1, 1),
    (2, 2),
    (3, 6),     # 3! = 6
    (5, 120),   # 5! = 120
])
def test_factorial(input, expected):
    assert factorial(input) == expected
```

## Mocking Examples

### Mock External API

```python
from unittest.mock import Mock, patch

def test_fetch_user_from_api(mock_http):
    # Mock API response
    mock_http.return_value = {"id": 1, "name": "Alice"}

    user = fetch_user(1)
    
    assert user["name"] == "Alice"

# Patch the module at import time
@patch('source.lib.requests.get')
def test_fetch_user(mock_get):
    mock_get.return_value = Mock(json=lambda: {"id": 1, "name": "Bob"})
    
    user = fetch_user(1)
    assert user["name"] == "Bob"
```

### Test State & Side Effects

```python
def test_counter_increments():
    counter = Counter()
    
    counter.increment()
    assert counter.value == 1
    
    counter.increment()
    assert counter.value == 2

def test_file_write_then_read(tmp_path):
    # tmp_path: pytest fixture for temporary directory
    file = tmp_path / "test.txt"
    file.write_text("Hello")
    
    assert file.read_text() == "Hello"
```

## Test Organization

```
source/
├── tests/
│   ├── __init__.py
│   ├── conftest.py           # Shared fixtures
│   └── unit/
│       ├── test_controllers/
│       ├── test_models/
│       ├── test_repositories/
│       └── test_services/
```

### conftest.py (Shared Fixtures)

```python
import pytest

@pytest.fixture(scope="session")
def test_database():
    """Session-scoped fixture for test database."""
    db = TestDatabase()
    db.setup()
    yield db
    db.teardown()
```

## Procedure

1. **Write a test first** (Test-Driven Development):
   ```python
   def test_fibonacci_sequence():
       assert fibonacci(0) == 0
       assert fibonacci(1) == 1
       assert fibonacci(5) == 5
   ```

2. **Run the test** (will fail):
   ```bash
   python -m pytest source/tests/unit/ -v -k test_fibonacci
   ```

3. **Implement the function** to make test pass

4. **Run all tests** and check coverage:
   ```bash
   python -m pytest source/tests/ --cov=source --cov-report=html
   ```

5. **Refactor** while keeping tests green

## Best Practices

- **One assertion per test** (or logically related assertions)
- **Clear test names**: `test_<function>_<scenario>_<expected_result>`
- **Test edge cases**: empty, None, negative, boundary values
- **Mock external dependencies**: APIs, files, databases
- **Keep tests fast**: <1ms per test, use fixtures
- **Avoid test interdependencies**: each test runs independently
- **DRY**: Use fixtures to reduce duplication

## References

- [pytest official documentation](./references/pytest-guide.md)
- [unittest standard library docs](https://docs.python.org/3/library/unittest.html)
- [Mock objects documentation](./references/mocking.md)
- [Test coverage best practices](./references/test-coverage.md)

## Tools Configuration

See [pytest.ini config](./scripts/pytest.ini) for pytest setup.

