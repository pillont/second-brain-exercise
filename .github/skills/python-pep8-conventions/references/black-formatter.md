# Black Formatter Configuration

## Installation

```bash
python -m pip install black
```

## Usage

```bash
# Format entire directory
python -m black source/

# Format specific file
python -m black source/lib/main.py

# Check without modifying (dry-run)
python -m black --check source/

# Show diff
python -m black --diff source/
```

## Configuration (pyproject.toml)

```toml
[tool.black]
line-length = 88
target-version = ['py310', 'py311']
include = '\.pyi?$'
exclude = '/\.git|venv|build|dist/'
```

## Key Features

- **Opinionated formatter**: Removes debates about style
- **Line length**: Defaults to 88 (vs PEP 8's 79)
- **String formatting**: Normalizes quotes and formatting
- **Trailing commas**: Adds for multi-line collections
- **Whitespace**: Normalizes spacing around operators

## Integration with Flake8

Black and Flake8 have minor conflicts:
- E203 (whitespace before `:` in slices) - IGNORE in Flake8
- W503 (line break before binary operator) - IGNORE in Flake8

## Modern Python Style

Black follows Python 3.6+ conventions:
- f-strings over `.format()`
- Type hints
- Walrus operator `:=` when appropriate
