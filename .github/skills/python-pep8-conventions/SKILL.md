---
name: python-pep8-conventions
description: "Ensure Python code follows PEP 8 style standards. Use when: formatting code, naming variables/functions, organizing imports, setting line lengths, writing docstrings, or enforcing code style consistency with linters."
argument-hint: "Optional: file path or module name to lint"
---

# Python PEP 8 Conventions

## When to Use

- Format code to comply with PEP 8 standard
- Establish naming conventions (snake_case for functions/variables, UPPER_CASE for constants)
- Organize and sort imports
- Enforce line length limits (79-88 characters)
- Structure docstrings and comments
- Configure linting tools (flake8, pylint)
- Review code style before committing

## PEP 8 Core Principles

### 1. Naming Conventions
- **Functions & variables**: `snake_case`
- **Constants**: `UPPER_CASE`
- **Classes**: `PascalCase`
- **Private**: Leading underscore `_private_method`
- **Avoid**: Single letter variables (except `i`, `j`, `k` in loops)

### 2. Indentation & Whitespace
- Use 4 spaces per indentation level (never tabs)
- Maximum line length: 79 characters (PEP 8 strict) or 88 characters (Black formatter)
- Two blank lines between top-level functions/classes
- One blank line between methods in a class
- No trailing whitespace

### 3. Imports
- Imports at top of file, after module docstring
- One import per line (except `from x import a, b`)
- Group in order: standard library → third-party → local
- Use absolute imports, relative imports only when necessary
- Write `from module import something`, not `import module.something`

### 4. Docstrings & Comments
- Module docstring at top, triple quotes `"""`
- Function docstrings: one line for simple, multi-line for complex
- Comment only non-obvious logic, not "obvious" code
- Use full sentences with proper grammar

### 5. Operators & Spacing
- Spaces around operators: `x = 1 + 2` (not `x=1+2`)
- No space around `=` in keyword arguments: `func(arg=value)`
- Space after commas: `[1, 2, 3]`

## Procedure

1. **Check current style** using [flake8 config](./scripts/.flake8)
   ```bash
   python -m flake8 source/
   ```

2. **Auto-format** (if using Black):
   ```bash
   python -m black source/
   ```

3. **Manually fix** remaining issues:
   - Review flake8 output for violations
   - Rename variables/functions to snake_case
   - Reorganize imports per PEP 8 groups
   - Add blank lines between definitions
   - Wrap long lines with backslash or parentheses

4. **Validate** with pylint for additional insights:
   ```bash
   python -m pylint source/ --disable=C0111
   ```

5. **Document** in code:
   - Always include module and function docstrings
   - Use type hints (see [python-typing skill](../python-typing/))

## References

- [PEP 8 Official](https://pep8.org/)
- [Official Python Enhancement Proposal 8](https://www.python.org/dev/peps/pep-0008/)
- [Flake8 Configuration](./references/flake8-config.md)
- [Auto-formatting with Black](./references/black-formatter.md)

## Tools Configuration

See [.flake8 config](./scripts/.flake8) and [pyproject.toml](./scripts/pyproject.toml) for linter setup.
