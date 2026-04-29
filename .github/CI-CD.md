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

## Local Development Setup

### Environment Setup

1. **Create and activate virtual environment**:
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Verify installation**:
```bash
python -c "import flask; print(f'Flask {flask.__version__} installed')"
```

### Running the API Locally

Start the development server:
```bash
python -m source.app
```

Expected output:
```
2026-04-29 10:15:30,127 - source - INFO - Creating Flask app in 'development' mode
2026-04-29 10:15:30,128 - source - INFO - Configuration loaded: DEBUG=True, TESTING=False
2026-04-29 10:15:30,129 - source - INFO - Registering blueprints...
2026-04-29 10:15:30,130 - source - INFO - Blueprints registered successfully
2026-04-29 10:15:30,131 - source - INFO - Flask app created successfully on development mode
2026-04-29 10:15:30,132 - source - INFO - Starting Flask server...
 * Running on http://127.0.0.1:5000
```

The API is now available at `http://localhost:5000`

### Testing the Local API

1. **Using curl**:
```bash
# Test the GET /hello endpoint
curl http://localhost:5000/hello

# Expected response:
# {"id":1,"message":"Hello from API!"}
```

2. **Using Python**:
```python
import requests
response = requests.get('http://localhost:5000/hello')
print(response.status_code)  # 200
print(response.json())       # {'id': 1, 'message': 'Hello from API!'}
```

### Logging During Development

**Console Logs**: All logs are printed to stdout during development.

**Log Format**: `timestamp - logger_name - level - message`

**Log Levels**:
- `INFO` (default) - General information about application flow
- `DEBUG` - Detailed debugging information
- `WARNING` - Warning messages
- `ERROR` - Error messages

**Change log level** in `source/config.py` by modifying the `DevelopmentConfig.LOG_LEVEL` setting.

### Next Steps

1. **Understand the architecture**: Read [Architecture Guide](../source/architecture.md) for details on the 5-layer MVC pattern
2. **Explore the code**:
   - `source/controllers/greeting_controller.py` - First example endpoint
   - `source/services/greeting_service.py` - Business logic layer
   - `source/models/greeting.py` - Domain model
3. **Add new endpoints**: Follow the pattern guide below
4. **Run tests**: See [Testing Guide](../source/tests/README.md) (future) for running unit tests

## Adding New Endpoints: Step-by-Step Pattern

Follow this pattern for all new endpoints:

### Step 1: Create Model (if needed)
File: `source/models/my_entity.py`
```python
from dataclasses import dataclass

@dataclass
class MyEntity:
    id: int
    name: str
```

### Step 2: Create Service
File: `source/services/my_service.py`
```python
import logging
from source.models.my_entity import MyEntity

logger = logging.getLogger(__name__)

class MyService:
    def get_entity(self, entity_id: int) -> MyEntity:
        logger.info(f"MyService.get_entity() called with id={entity_id}")
        # Business logic here
        return MyEntity(id=entity_id, name="Example")
```

### Step 3: Register Service in Container
File: `source/container.py`
```python
from source.services.my_service import MyService

class Container(containers.DeclarativeContainer):
    my_service = providers.Singleton(MyService)
    greeting_service = providers.Singleton(GreetingService)
```

### Step 4: Create Controller
File: `source/controllers/my_controller.py`
```python
import logging
from flask import Blueprint, jsonify, Response
from dependency_injector.wiring import inject, Provide
from source.container import Container

logger = logging.getLogger(__name__)

my_bp = Blueprint('my', __name__, url_prefix='')

@my_bp.route('/entities/<int:entity_id>', methods=['GET'])
@inject
def get_entity(
    entity_id: int,
    my_service=Provide[Container.my_service],
) -> Response:
    logger.info(f"GET /entities/{entity_id} endpoint called")
    try:
        entity = my_service.get_entity(entity_id)
        return jsonify(entity.__dict__), 200
    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=True)
        return jsonify({'error': 'Internal server error'}), 500
```

### Step 5: Wire Controller in App
File: `source/__init__.py` in `setup_container()`:
```python
container.wire(modules=[
    'source.controllers.greeting_controller',
    'source.controllers.my_controller',  # Add this
])
```

### Step 6: Register Blueprint
File: `source/__init__.py` in `create_app()`:
```python
from source.controllers.my_controller import my_bp
app.register_blueprint(my_bp)
```

### Step 7: Test
```bash
python -m source.app
curl http://localhost:5000/entities/1
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
