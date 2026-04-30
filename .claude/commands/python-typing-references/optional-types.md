# Managing Optional Types in Python

## Basic Optional Pattern

```python
from typing import Optional

# Optional[T] = Union[T, None]
def get_user_email(user_id: int) -> Optional[str]:
    if user_id > 0:
        return "user@example.com"
    return None

# Caller must handle None
email = get_user_email(1)
if email is not None:
    print(f"Email: {email}")
```

## Avoiding Optional with Default Values

```python
from typing import Literal

# Instead of Optional, provide default
def get_user_name(user_id: int, default: str = "Unknown") -> str:
    if user_id > 0:
        return "John"
    return default

# Always returns str, never None
name = get_user_name(1)  # Safe: no None possibility
```

## Using None Coalescing

```python
# Python 3.9+: walrus operator
if (email := get_user_email(1)) is not None:
    print(f"Email: {email}")

# Python 3.10+: match statement
match get_user_email(1):
    case str(email):
        print(f"Email: {email}")
    case None:
        print("No email found")
```

## Type Narrowing

```python
from typing import Union

def process(value: Union[str, int, None]) -> None:
    if value is None:
        print("No value")
        return
    
    # Type narrowed to Union[str, int]
    if isinstance(value, str):
        print(f"String: {value}")
    elif isinstance(value, int):
        print(f"Number: {value}")
```

## Asserting Non-None

```python
from typing import Optional

def get_data() -> Optional[str]:
    return "data"

data = get_data()
assert data is not None  # Type narrowed to str
print(data.upper())  # MyPy accepts this
```

## Common Optional Anti-patterns

❌ **Don't**: Return mutable default (sentinel)
```python
def get_items(user_id: int) -> List[str]:
    return None  # Type says List, returns None!
```

✅ **Do**: Return empty list or raise exception
```python
def get_items(user_id: int) -> List[str]:
    return []  # Type matches return

def get_required_items(user_id: int) -> List[str]:
    items = fetch_from_db(user_id)
    if not items:
        raise ValueError(f"No items for user {user_id}")
    return items
```
