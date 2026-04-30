# Flake8 Configuration Reference

## Usage

```bash
python -m flake8 source/
python -m flake8 source/lib/main.py
python -m flake8 source/ --show-source  # Show violation source lines
```

## Configuration Fields

- **max-line-length**: Maximum allowed line length (default: 79)
- **extend-ignore**: Error codes to ignore (E203, W503)
- **exclude**: Directories/files to skip
- **per-file-ignores**: Error codes to ignore in specific files

## Common Error Codes

- `E1`: Indentation errors
- `E2`: Whitespace errors
- `E3`: Blank line errors
- `W2`: Whitespace warnings
- `W3`: Blank line warnings
- `W6`: Deprecation warnings
- `F8`: Name errors, undefined, duplicated
-`C9`: Complexity warnings

## Example: Configure for project

```bash
# Install
python -m pip install flake8

# Run with output
python -m flake8 source/ --statistics --count
```

## Fixing Common Issues

| Error | Fix |
|-------|-----|
| Line too long | Split using `\` or parentheses |
| Multiple statements on one line | Put each statement on new line |
| Trailing whitespace | Remove spaces at end of line |
| Multiple imports per line | Use one import per line |
