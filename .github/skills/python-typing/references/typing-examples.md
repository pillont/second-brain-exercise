# Type Hints Examples for Python

## Basic Type Hints

```python
from typing import Optional, List, Dict, Any

# Function with type hints
def greet(name: str) -> str:
    return f"Hello, {name}!"

# Multiple parameters
def add(a: int, b: int) -> int:
    return a + b

# Return None
def print_message(msg: str) -> None:
    print(msg)

# Optional return
def find_user(user_id: int) -> Optional[Dict[str, Any]]:
    if user_id > 0:
        return {"id": user_id, "name": "User"}
    return None
```

## Collections with Type Parameters

```python
from typing import List, Dict, Set, Tuple

# List
numbers: List[int] = [1, 2, 3]
strings: List[str] = ["a", "b", "c"]

# Dictionary
mapping: Dict[str, int] = {"a": 1, "b": 2}

# Set
unique: Set[str] = {"x", "y", "z"}

# Tuple
pair: Tuple[str, int] = ("name", 42)
triple: Tuple[int, int, int] = (1, 2, 3)
```

## Union Types

```python
from typing import Union

# Variable can be int or str
value: Union[int, str] = 42
value = "text"

# Function returns int or None
def maybe_divide(a: int, b: int) -> Union[int, None]:
    return a // b if b != 0 else None

# Alternative: Optional (for None)
def maybe_divide_v2(a: int, b: int) -> Optional[int]:
    return a // b if b != 0 else None
```

## Callable Types

```python
from typing import Callable

# Function that takes callback
def apply_operation(func: Callable[[int, int], int], x: int, y: int) -> int:
    return func(x, y)

# Usage
result = apply_operation(lambda a, b: a + b, 5, 3)  # result = 8
```

## Type Aliases

```python
UserId = int
UserData = Dict[str, Any]

def get_user(user_id: UserId) -> UserData:
    return {"id": user_id, "name": "Bob"}
```

## Class Type Hints

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
        return {
            "name": self.name,
            "age": self.age
        }

    def set_email(self, email: str) -> None:
        self.email = email
```

## Generic Classes

```python
from typing import Generic, TypeVar

T = TypeVar('T')  # Generic type variable

class Container(Generic[T]):
    def __init__(self, value: T) -> None:
        self.value = value

    def get(self) -> T:
        return self.value

# Usage
int_container: Container[int] = Container(42)
str_container: Container[str] = Container("hello")
```

## Protocols (Structural Typing)

```python
from typing import Protocol

class Drawable(Protocol):
    def draw(self) -> None: ...

class Circle:
    def draw(self) -> None:
        print("Drawing circle")

def render(obj: Drawable) -> None:
    obj.draw()

# Works even though Circle doesn't inherit from Drawable
render(Circle())
```
