# GitHub Actions & CI/CD Setup

## Overview

This project uses GitHub Actions to automatically verify code quality on every push and pull request. The workflow ensures:

✅ Code follows PEP 8 style standards (Black, Flake8)
✅ Type hints are correct (MyPy)
✅ Tests pass (Unit & Integration)
✅ Code coverage meets targets (>80%)
✅ Code complexity is acceptable (Radon)

## Files

- **Workflow**: `.github/workflows/quality-checks.yml` — Main CI/CD workflow
- **Pre-commit config**: `.pre-commit-config.yaml` — Local development hooks
- **Documentation**: [CI/CD Guide](.github/skills/python-pep8-conventions/references/ci-cd-workflow.md)

## Quick Setup

### For Repository Maintainers

The workflow runs automatically. No setup needed.

**To view results**:
1. Go to GitHub → Actions tab
2. Click on the workflow run
3. View logs and check which step failed (if any)
4. Download coverage artifacts

### For Local Development

Set up pre-commit hooks to catch issues before pushing:

```bash
# Install pre-commit
pip install pre-commit

# Install git hooks
pre-commit install

# Now hooks run automatically on each commit
git commit -m "my changes"  # Black, Flake8, MyPy run here
```

To run hooks manually:
```bash
pre-commit run --all-files
```

---

## Workflow Behavior

### On a New Push/PR

1. GitHub Actions triggers automatically
2. Matrix runs tests on Python 3.10 and 3.11
3. Each job reports status:
   - **Green** ✅ = Passed
   - **Red** ❌ = Failed
4. PR shows status check before merge option

### If a Check Fails

**Example**: Flake8 fails with "Line too long"

```bash
# 1. See failure in GitHub Actions log
# 2. Run locally to reproduce
python -m flake8 source/

# 3. Fix issue (auto-format with Black)
python -m black source/

# 4. Verify fixed
python -m flake8 source/

# 5. Commit and push
git commit -am "Fix code style"
git push
```

### Artifacts

After each run, **coverage reports** are available:
1. Go to GitHub Actions run
2. Scroll to "Artifacts" section
3. Download `coverage-report-3.10.zip` or `coverage-report-3.11.zip`
4. Extract and view `htmlcov/index.html` in browser

## Quality Checks Explained

### 1. Black (Code Formatting)
Ensures consistent code style.

**Failure example**:
```
error: 1 file would be reformatted
```

**Fix**:
```bash
python -m black source/
```

### 2. Flake8 (PEP 8 Style)
Checks code style compliance.

**Failure example**:
```
source/lib/main.py:42:E501 line too long (95 > 88 characters)
```

**Fix**: Split long lines or let Black handle it.

### 3. MyPy (Type Checking)
Validates type hints.

**Failure example**:
```
source/lib/main.py:10: error: Argument 1 to "func" has incompatible type "str"; expected "int"
```

**Fix**: Check function signature vs. caller.

### 4. Pytest (Unit Tests)
Runs unit tests with coverage.

**Failure example**:
```
FAILED source/lib_test/unit/test_main.py::TestClass::test_method
AssertionError: assert 5 == 6
```

**Fix**: Update test or code logic.

### 5. Pytest (Integration Tests)
Runs integration tests.

**Failure example**:
```
FAILED source/lib_test/integration/test_workflow.py::test_user_creation
  Connection refused: mock API unreachable
```

**Fix**: Check mock setup or database connection.

## Branch Protection Rules

Recommended GitHub settings to enforce CI/CD:

1. Go to **Repository → Settings → Branches**
2. Add rule for `main` branch:
   - ✅ Require status checks to pass
   - ✅ Require branch to be up to date
   - ✅ Require code reviews before merge
   - ✅ Restrict who can push (optional)

This prevents direct pushes to `main` and requires CI to pass.

## Troubleshooting

### "Action failed on main branch"

Check the workflow run:
```bash
# View last workflow in GitHub
# or run locally to debug
python -m flake8 source/
python -m mypy source/
pytest source/lib_test/
```

### "Pre-commit hook failed locally"

Run the hook manually:
```bash
pre-commit run --all-files
```

Fix issues and commit again.

### "Coverage below 80%"

See coverage report:
```bash
python -m pytest source/lib_test/ --cov=source/lib --cov-report=html
open htmlcov/index.html
```

Add tests for uncovered lines.

### "Matrix fails on 3.11 but passes on 3.10"

Check Python version compatibility:
```bash
python3.11 -m pytest source/lib_test/
```

Fix compatibility issues in code.

## Advanced: Customizing Workflow

Edit `.github/workflows/quality-checks.yml`:

**Add new tool**:
```yaml
- name: Run custom check
  run: |
    python -m custom_tool source/
```

**Add new branch**:
```yaml
on:
  push:
    branches: [ main, develop, staging ]
```

**Change Python versions**:
```yaml
matrix:
  python-version: ['3.10', '3.11', '3.12']
```

## Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Pre-commit Documentation](https://pre-commit.com/)
- [Black Documentation](https://black.readthedocs.io/)
- [Flake8 Documentation](https://flake8.pycqa.org/)
- [MyPy Documentation](https://mypy.readthedocs.io/)
- [Pytest Documentation](https://docs.pytest.org/)
