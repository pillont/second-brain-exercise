# MyPy Type Checker Guide

## Installation

```bash
python -m pip install mypy
```

## Usage

```bash
# Check entire project
python -m mypy source/

# Check specific file
python -m mypy source/lib/main.py

# Strict mode (most checking)
python -m mypy source/ --strict

# Allow dynamic typing
python -m mypy source/

# Show error codes
python -m mypy source/ --show-error-codes
```

## Configuration (mypy.ini)

Key options:
- `python_version`: Target Python version (3.10, 3.11, etc.)
- `warn_return_any`: Warn when returning `Any` type
- `disallow_untyped_defs`: Require type hints on all definitions
- `strict_optional`: Enforce `Optional` for nullable types
- `strict_equality`: Check equality with incompatible types

## Common MyPy Errors

| Error | Fix |
|-------|-----|
| `error: Argument 1 to "X" has incompatible type "Y"` | Check function signature, adjust type |
| `error: Missing return statement` | Add `return` or `-> None` |
| `error: Name "X" is not defined` | Import missing module or define variable |
| `error: Incompatible return value type` | Match return type to annotation |
| `error: Expected "Y", got "X"` | Type mismatch, cast or convert |

## Type Checking Levels

1. **Basic** (default): Check function signatures, obvious errors
2. **Strict Mode** (`--strict`): Check all types, all definitions, all imports
3. **Custom**: Use mypy.ini for selective strict checking

## Integration with IDE

Most IDEs (PyCharm, VS Code) integrate MyPy for real-time type checking.
