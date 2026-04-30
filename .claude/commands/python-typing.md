---
name: python-typing
description: "Add type annotations to Python code using type hints and MyPy static analysis. Use when: annotating function parameters, return types, variables, generics, handling Optional/Union types, or validating code with MyPy type checker."
argument-hint: "Optional: file path to add type annotations"
---

# Python Type Hints & Typing

## When to Use

- Add type annotations to functions, methods, and variables
- Use generics for collections (`List[str]`, `Dict[str, int]`)
- Handle nullable values with `Optional[T]`
- Create type aliases for complex types
- Run MyPy static type checker for type validation
- Improve IDE autocompletion and error detection
- Document expected types in code

## Type Annotation Basics

### 1. Function Annotations
```python
def greet(name: str) -> str:
    """Greet someone by name."""
    return f"Hello, {name}!"

def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

def fetch_user(user_id: int) -> Optional[dict]:
    """Fetch user data or None if not found."""
    return None if user_id < 0 else {"id": user_id}
```

### 2. Variable Type Hints
```python
# Explicit type assignment
count: int = 0
name: str = "Alice"
values: List[int] = [1, 2, 3]
mapping: Dict[str, int] = {"a": 1}

# Type aliases for readability
UserId = int
UserData = Dict[str, Any]

current_user: UserData = {"name": "Bob", "id": 42}
```

### 3. Generics & Collections
```python
from typing import List, Dict, Set, Tuple, Optional, Union

# Basic collections
numbers: List[int] = [1, 2, 3]
name_to_age: Dict[str, int] = {"Alice": 30}
unique_ids: Set[str] = {"id1", "id2"}
pair: Tuple[str, int] = ("name", 42)

# Optional (nullable)
maybe_value: Optional[str] = None  # Same as Union[str, None]

# Union types
result: Union[int, str] = 42  # Can be int or str
status: Union[int, None] = None
```

### 4. Class Type Hints
```python
from typing import Any

class User:
    name: str
    age: int
    email: Optional[str] = None

    def __init__(self, name: str, age: int) -> None:
        self.name = name
        self.age = age

    def get_info(self) -> Dict[str, Any]:
        """Return user info as dictionary."""
        return {"name": self.name, "age": self.age}
```

### 5. Callable Types
```python
from typing import Callable

# Function type parameter
def apply_function(func: Callable[[int, int], int], a: int, b: int) -> int:
    return func(a, b)

# Callback parameter
def process(callback: Callable[[str], None]) -> None:
    callback("data processed")
```

## Procedure

1. **Install MyPy** (if not present):
   ```bash
   python -m pip install mypy
   ```

2. **Add type hints incrementally**:
   - Start with function signatures (parameters + return)
   - Move to class attributes and methods
   - Add complex types (`List`, `Dict`, `Optional`)
   - Use type aliases for repeated complex types

3. **Run MyPy validation**:
   ```bash
   python -m mypy source/ --strict
   ```

4. **Fix type errors**:
   - Review MyPy output, understand type mismatches
   - Update annotations or code logic
   - Use `# type: ignore` sparingly for legitimate exceptions

5. **Document with comments** when types are unclear:
   ```python
   def process(data: Union[str, bytes]) -> List[str]:
       # data can be string or bytes, returns list of strings
       ...
   ```

## Advanced: Protocols & Generics

```python
from typing import TypeVar, Generic, Protocol

# Generic type variable
T = TypeVar('T')

class Container(Generic[T]):
    def __init__(self, value: T) -> None:
        self.value = value

    def get(self) -> T:
        return self.value

# Protocol (structural typing)
class Readable(Protocol):
    def read(self) -> str: ...

def process_readable(reader: Readable) -> None:
    content = reader.read()
    print(content)
```

## References

- [Official Python typing module](https://docs.python.org/3/library/typing.html)
- [MyPy documentation](./python-typing-references/mypy-guide.md)
- [Type hints examples](./python-typing-references/typing-examples.md)
- [Managing Optional types](./python-typing-references/optional-types.md)

## Tools Configuration

See [mypy.ini config](./python-typing-scripts/mypy.ini) for MyPy setup.
