---
name: python-integration-testing
description: "Write integration tests for Python features that interact with external systems (APIs, databases, services). Use when: testing module interactions, mocking external APIs, testing database queries, verifying end-to-end workflows, or testing with multiple components together."
argument-hint: "Optional: integration test file or feature name"
---

# Python Integration Testing

## When to Use

- Test interactions between multiple modules/components
- Test with mocked external APIs (HTTP endpoints, databases)
- Verify feature workflows end-to-end
- Test error handling during external service failures
- Validate data flow through system components
- Test async operations and callbacks
- Ensure feature completeness before deployment

## Integration Testing vs Unit Testing

| Aspect | Unit Test | Integration Test |
|--------|-----------|-----------------|
| Scope | Single function | Multiple components |
| Speed | Fast (<1ms) | Slower (100ms+) |
| Dependencies | Mocked | Real or mocked services |
| Focus | Logic correctness | Component interaction |
| Frequency | Run on every commit | Run on pull requests |

## Integration Testing Patterns

### 1. Mock External APIs

```python
import pytest
from unittest.mock import Mock, patch
import requests

@pytest.fixture
def mock_api():
    """Mock external API responses."""
    with patch('requests.get') as mock_get:
        mock_response = Mock()
        mock_response.json.return_value = {
            "id": 1,
            "name": "Alice",
            "email": "alice@example.com"
        }
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        yield mock_get

def test_user_service_with_mocked_api(mock_api):
    """Test UserService with mocked external API."""
    from source.lib.user_service import UserService
    
    service = UserService()
    user = service.get_user(1)
    
    assert user["name"] == "Alice"
    mock_api.assert_called_once_with("https://api.example.com/users/1")

def test_api_error_handling(mock_api):
    """Test error handling when API fails."""
    mock_api.side_effect = requests.ConnectionError("API unreachable")
    
    from source.lib.user_service import UserService
    service = UserService()
    
    with pytest.raises(ServiceError):
        service.get_user(1)
```

### 2. Database Integration Tests

```python
import pytest
from source.lib.models import User
from source.lib.database import Database

@pytest.fixture
def test_db():
    """Fixture: in-memory test database."""
    db = Database(":memory:")  # SQLite in-memory
    db.setup_schema()
    yield db
    db.close()

class TestUserRepository:
    def test_create_and_retrieve_user(self, test_db):
        """Test creating and retrieving user from database."""
        # ARRANGE
        repo = UserRepository(test_db)
        new_user = User(name="Bob", email="bob@example.com")
        
        # ACT
        user_id = repo.create(new_user)
        retrieved_user = repo.get(user_id)
        
        # ASSERT
        assert retrieved_user.name == "Bob"
        assert retrieved_user.email == "bob@example.com"
    
    def test_update_user(self, test_db):
        """Test updating user in database."""
        repo = UserRepository(test_db)
        user = User(name="Charlie", email="charlie@example.com")
        user_id = repo.create(user)
        
        # Update user
        user.email = "charlie_new@example.com"
        repo.update(user)
        
        # Verify update
        updated_user = repo.get(user_id)
        assert updated_user.email == "charlie_new@example.com"
    
    def test_delete_user(self, test_db):
        """Test deleting user from database."""
        repo = UserRepository(test_db)
        user = User(name="Diana", email="diana@example.com")
        user_id = repo.create(user)
        
        repo.delete(user_id)
        assert repo.get(user_id) is None
```

### 3. Multi-Component Workflow Tests

```python
import pytest
from unittest.mock import Mock, patch
from source.lib.user_manager import UserManager
from source.lib.notification_service import NotificationService

@pytest.fixture
def mock_email_service():
    """Mock email sending service."""
    with patch('source.lib.notification_service.send_email') as mock:
        yield mock

def test_user_registration_workflow(mock_email_service, test_db):
    """Test complete user registration workflow."""
    # ARRANGE
    manager = UserManager(test_db)
    notify = NotificationService()
    
    # ACT: Register user
    user_id = manager.register(
        name="Eve",
        email="eve@example.com",
        password="secure123"
    )
    
    # Notify user
    notify.send_welcome_email("eve@example.com")
    
    # ASSERT: User created in database
    user = manager.get_user(user_id)
    assert user is not None
    assert user.name == "Eve"
    
    # ASSERT: Notification sent
    mock_email_service.assert_called_once()
    call_args = mock_email_service.call_args
    assert "eve@example.com" in str(call_args)
```

### 4. Testing Async Operations

```python
import pytest
import asyncio
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_async_data_fetch():
    """Test async API call."""
    with patch('aiohttp.ClientSession.get') as mock_get:
        mock_response = AsyncMock()
        mock_response.json = AsyncMock(return_value={"status": "ok"})
        mock_get.return_value = mock_response
        
        from source.lib.async_client import AsyncClient
        client = AsyncClient()
        result = await client.fetch_data()
        
        assert result["status"] == "ok"
```

### 5. Feature Integration Tests

```python
import pytest
from source.lib.fizz_buzz import FizzBuzzGame

class TestFizzBuzzFeature:
    """Test FizzBuzz game feature end-to-end."""
    
    def test_fizz_buzz_1_to_100(self):
        """Test FizzBuzz output for 1-100 range."""
        game = FizzBuzzGame()
        output = game.play(1, 100)
        
        lines = output.split('\n')
        
        # Verify specific values
        assert lines[2] == "Fizz"      # 3
        assert lines[4] == "Buzz"      # 5
        assert lines[14] == "FizzBuzz" # 15
    
    def test_fizz_buzz_custom_rules(self):
        """Test FizzBuzz with custom rules."""
        game = FizzBuzzGame()
        game.add_rule(7, "Whizz")
        output = game.play(1, 50)
        
        # 35 = 5 * 7, should be "BuzzWhizz"
        assert "BuzzWhizz" in output
```

## Test Organization

```
source/
├── tests/
│   ├── conftest.py              # Shared fixtures
│   ├── unit/
│   │   ├── test_controllers/
│   │   ├── test_models/
│   │   ├── test_repositories/
│   │   └── test_services/
│   └── integration/
│       ├── test_user_workflow.py
│       ├── test_api_integration.py
│       └── test_database.py
```

### conftest.py (Integration Fixtures)

```python
import pytest
from unittest.mock import Mock

@pytest.fixture(scope="session")
def integration_config():
    """Session-scoped config for integration tests."""
    return {
        "database_url": "sqlite:///:memory:",
        "api_timeout": 5,
        "mock_external_apis": True
    }

@pytest.fixture
def mock_external_service():
    """Mock all external services."""
    with patch.dict('os.environ', {
        'API_BASE_URL': 'https://mock.example.com',
        'DB_URL': 'sqlite:///:memory:'
    }):
        yield
```

## Procedure

1. **Identify feature to test**:
   - What components interact?
   - What external services are involved?
   - What's the happy path and error cases?

2. **Create integration test file**:
   ```python
   # source/lib_test/integration/test_feature.py
   import pytest
   
   class TestFeatureName:
       def test_happy_path(self):
           # Test successful workflow
           pass
       
       def test_error_handling(self):
           # Test failure scenarios
           pass
   ```

3. **Mock external dependencies**:
   ```python
   @patch('external_api.request')
   def test_with_mocked_api(mock_api):
       mock_api.return_value = {"status": "ok"}
       # Test implementation
   ```

4. **Run integration tests**:
   ```bash
   python -m pytest source/tests/integration/ -v
   ```

5. **Verify coverage**:
   ```bash
   python -m pytest source/tests/ --cov=source --cov-report=term-missing
   ```

## Best Practices

- **Mock external services** to keep tests deterministic and fast
- **Test both success and failure paths** (API down, timeouts, invalid data)
- **Use fixtures** for shared database/API setup
- **Separate unit and integration tests** (different directories)
- **Keep integration tests focused** on component interactions, not unit logic
- **Document assumptions** about external services and APIs
- **Run integration tests in CI/CD pipeline** before deployment

## References

- [pytest integration testing guide](./references/integration-guide.md)
- [Mock/patch for external services](./references/mocking-external-services.md)
- [Database testing patterns](./references/database-testing.md)
- [Async testing with pytest-asyncio](./references/async-testing.md)

## Tools Configuration

See [pytest.ini config](../python-unit-testing/scripts/pytest.ini) for pytest setup (shared with unit tests).
