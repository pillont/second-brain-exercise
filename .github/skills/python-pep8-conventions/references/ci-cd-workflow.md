# CI/CD & GitHub Actions

## GitHub Actions Workflow

A workflow is configured at `.github/workflows/quality-checks.yml` to automatically check code quality on every push and pull request.

### Workflow Triggers

```yaml
on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]
```

Triggered on:
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop` branches
- Changes to `source/` directory

### Quality Checks Performed

| Check | Tool | Purpose |
|-------|------|---------|
| Code Formatting | black | Ensure consistent style |
| Style Compliance | flake8 | PEP 8 adherence |
| Type Validation | mypy | Type hint correctness |
| Unit Tests | pytest | Test functionality |
| Integration Tests | pytest | Component interaction |
| Code Complexity | radon | Cyclomatic complexity |
| Code Analysis | pylint | Additional issues |
| Coverage Reports | pytest-cov | Test coverage metrics |

### Workflow Steps

1. **Setup Python** — Installs Python 3.10 and 3.11
2. **Install Dependencies** — Installs all required tools
3. **Black Check** — Verify code formatting matches Black style
4. **Flake8 Lint** — Check PEP 8 compliance
5. **MyPy Type Check** — Validate type hints
6. **Unit Tests** — Run unit tests with coverage
7. **Integration Tests** — Run integration tests
8. **Complexity Analysis** — Report code complexity (radon)
9. **Pylint Analysis** — Additional lint checks
10. **Coverage Reports** — Upload coverage artifacts

### Required Status Checks

For Pull Requests to merge, all required checks must pass:
- ✅ Black formatting
- ✅ Flake8 (PEP 8)
- ✅ MyPy (types)
- ✅ Unit tests (>80% coverage)
- ✅ Integration tests

### Workflow Output

On failure, the workflow will:
1. Show error details with line numbers
2. Report which check failed
3. Provide actionable error messages
4. Block PR merge until resolved

Example error:
```
Flake8 violation: E501 line too long (95 > 88 characters)
  source/lib/main.py:42
```

## Pre-commit Hooks (Local Development)

Set up local pre-commit hooks to catch issues before pushing to GitHub.

### Installation

```bash
# Install pre-commit framework
pip install pre-commit

# Install the git hook scripts
pre-commit install
```

### Configuration

Hooks are defined in `.pre-commit-config.yaml`:
- Black (code formatter)
- isort (import sorter)
- Flake8 (PEP 8)
- MyPy (type checker)
- Trailing whitespace cleanup
- File ending fixes

### Usage

```bash
# Run on all files before committing (automatic)
git add .
git commit -m "message"  # Hooks run automatically

# Run on specific file before committing
pre-commit run --files source/lib/main.py

# Run on all files (manual)
pre-commit run --all-files

# Skip hooks (not recommended)
git commit --no-verify
```

### Bypass Hooks

If necessary (rare):
```bash
git commit --no-verify
```

But preferably, fix issues and run hooks:
```bash
pre-commit run --all-files
# Fix reported issues
git add .
git commit -m "Fix code style"
```

## Continuous Integration Best Practices

1. **Small commits** — Easier to debug if a test fails
2. **Run tests locally first** — Before pushing
3. **Use pre-commit hooks** — Catch issues early
4. **Read CI logs** — Understand what failed
5. **Fix in feature branch** — Before merging to main

## Example: Fix Failing CI

1. See CI failure: "Flake8: Line too long"
2. Run locally: `python -m flake8 source/`
3. Fix issue: Split long line or use Black formatter
4. Verify: `python -m black source/`
5. Commit and push
6. CI automatically re-runs and passes ✅

## Configuration Files

- **Workflow**: `.github/workflows/quality-checks.yml`
- **Pre-commit**: `.pre-commit-config.yaml`
- **Black**: `.github/skills/python-pep8-conventions/scripts/pyproject.toml`
- **Flake8**: `.github/skills/python-pep8-conventions/scripts/.flake8`
- **MyPy**: `.github/skills/python-typing/scripts/mypy.ini`
- **Pytest**: `.github/skills/python-unit-testing/scripts/pytest.ini`
