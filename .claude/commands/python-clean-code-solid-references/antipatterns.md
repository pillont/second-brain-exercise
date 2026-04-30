# Python Anti-patterns to Avoid

## 1. Using Mutable Default Arguments

❌ **Bad**: List/dict are created once and shared

```python
def add_to_list(item, items=[]):
    items.append(item)
    return items

result1 = add_to_list(1)  # [1]
result2 = add_to_list(2)  # [1, 2] - SHARED!
```

✅ **Good**: Use None and create new list

```python
def add_to_list(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items

result1 = add_to_list(1)  # [1]
result2 = add_to_list(2)  # [2] - Independent
```

## 2. Not Using Context Managers

❌ **Bad**: Manual resource management

```python
file = open("data.txt")
data = file.read()
file.close()  # Might not execute if exception occurs
```

✅ **Good**: Use context manager

```python
with open("data.txt") as file:
    data = file.read()
# File auto-closed, even on exception
```

## 3. Bare Except Clauses

❌ **Bad**: Catches all exceptions including SystemExit

```python
try:
    dangerous_operation()
except:  # NEVER do this!
    print("Error")
```

✅ **Good**: Catch specific exceptions

```python
try:
    dangerous_operation()
except FileNotFoundError:
    print("File not found")
except ValueError as e:
    print(f"Value error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## 4. Modifying List While Iterating

❌ **Bad**: Skips elements or causes errors

```python
items = [1, 2, 3, 4, 5]
for item in items:
    if item % 2 == 0:
        items.remove(item)  # DON'T DO THIS!
```

✅ **Good**: Create new list or iterate over copy

```python
items = [1, 2, 3, 4, 5]

# Solution 1: List comprehension
items = [item for item in items if item % 2 != 0]

# Solution 2: Iterate over copy
for item in items[:]:
    if item % 2 == 0:
        items.remove(item)
```

## 5. Using `eval()` or `exec()`

❌ **Bad**: Security risk and bad practice

```python
user_code = "1 + 1"
result = eval(user_code)  # SECURITY HOLE!

# User could do: __import__('os').system('rm -rf /')
```

✅ **Good**: Use safer alternatives

```python
# For mathematical expressions
from ast import literal_eval
data = literal_eval("[1, 2, 3]")

# For user code, use restricted environment
import operator
allowed_ops = {
    'add': operator.add,
    'mul': operator.mul,
}
```

## 6. Global Variables

❌ **Bad**: Hard to test and debug

```python
config = {}

def load_config():
    global config
    config = {"debug": True}

def use_config():
    print(config["debug"])  # Depends on global state
```

✅ **Good**: Dependency injection

```python
class Config:
    def __init__(self, debug=False):
        self.debug = debug

def use_config(config: Config):
    print(config.debug)

config = Config(debug=True)
use_config(config)
```

## 7. Ignoring Exceptions

❌ **Bad**: Silently fails

```python
try:
    critical_operation()
except:
    pass  # Silent failure!
```

✅ **Good**: Log or handle gracefully

```python
import logging

try:
    critical_operation()
except ExceptionType as e:
    logging.error(f"Operation failed: {e}")
    # Re-raise if critical, or handle gracefully
    raise

# Or handle locally
try:
    critical_operation()
except FileNotFoundError:
    logging.warning("Config file missing, using defaults")
    use_defaults()
```

## 8. Not Using String Formatting

❌ **Bad**: String concatenation

```python
msg = "User " + name + " logged in at " + str(time)
```

✅ **Good**: f-strings (Python 3.6+)

```python
msg = f"User {name} logged in at {time}"

# Or format() for compatibility
msg = "User {} logged in at {}".format(name, time)
```

## 9. Using `is` for Value Comparison

❌ **Bad**: Checks identity, not equality

```python
if x is 5:  # WRONG! Checks if same object
    pass

if x is None:  # Correct for None
    pass
```

✅ **Good**: Use `==` for values

```python
if x == 5:  # Correct
    pass

if x is None:  # Still correct for None
    pass
```

## 10. Creating Unnecessary Classes

❌ **Bad**: Over-engineering

```python
class DataHolder:
    def __init__(self, value):
        self.value = value

holder = DataHolder(42)
```

✅ **Good**: Use simpler structures

```python
# Use dictionary
data = {"value": 42}

# Or dataclass for complex data
from dataclasses import dataclass

@dataclass
class Data:
    value: int

data = Data(value=42)
```
