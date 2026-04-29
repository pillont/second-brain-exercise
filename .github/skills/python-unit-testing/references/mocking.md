# Mocking Guide for Unit Tests

## Basic Mocking

```python
from unittest.mock import Mock, patch, call

# Create a mock object
mock_db = Mock()
mock_db.save.return_value = True

# Call it
result = mock_db.save({"id": 1})
print(result)  # True

# Verify it was called
mock_db.save.assert_called_once()
mock_db.save.assert_called_with({"id": 1})
```

## Patching Functions

```python
from unittest.mock import patch

@patch('requests.get')
def test_with_patch(mock_get):
    mock_get.return_value.json.return_value = {"status": "ok"}
    
    response = requests.get("http://example.com")
    data = response.json()
    
    assert data["status"] == "ok"
    mock_get.assert_called_once_with("http://example.com")

# Or use context manager
def test_with_context():
    with patch('requests.get') as mock_get:
        mock_get.return_value.json.return_value = {"status": "ok"}
        # Test code here
        pass
```

## Mock Assertions

```python
mock = Mock()
mock.method(1, 2)
mock.method(3, 4)

# Verify calls
mock.method.assert_called_once()  # Called exactly once
mock.method.assert_called_with(3, 4)  # Last call was with these args
mock.method.assert_any_call(1, 2)  # Was called with these args at some point
mock.method.assert_has_calls([
    call(1, 2),
    call(3, 4)
])  # Called in this sequence

# Check call count
assert mock.method.call_count == 2
```

## Mock Side Effects

```python
mock = Mock()

# Return different values on successive calls
mock.side_effect = [1, 2, 3]
print(mock())  # 1
print(mock())  # 2
print(mock())  # 3

# Raise exception on call
mock.side_effect = ValueError("Invalid")
mock()  # Raises ValueError

# Use callable for dynamic behavior
mock.side_effect = lambda x: x * 2
print(mock(5))  # 10
```

## MagicMock vs Mock

```python
from unittest.mock import Mock, MagicMock

# Mock: basic mock object
m = Mock()
m.any_method()  # Works

# MagicMock: supports magic methods (__str__, __repr__, etc.)
mm = MagicMock()
str(mm)  # Works
len(mm)  # Works

# Use MagicMock for file-like objects, dicts, etc.
mock_file = MagicMock()
mock_file.read.return_value = "file content"
```

## Mocking Class Instances

```python
from unittest.mock import patch

class Database:
    def save(self, data):
        pass

@patch('module.Database')
def test_with_mocked_class(mock_db_class):
    mock_instance = Mock()
    mock_db_class.return_value = mock_instance
    mock_instance.save.return_value = True
    
    # Your code that uses Database
    db = Database()
    result = db.save({"id": 1})
    
    assert result is True
    mock_instance.save.assert_called_once()
```
