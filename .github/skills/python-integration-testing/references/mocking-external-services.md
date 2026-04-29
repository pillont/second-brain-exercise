# Mocking External Services

## HTTP Requests with responses

```python
import pytest
import requests
from responses import matchers

@pytest.fixture
def mock_github_api():
    """Mock GitHub API responses."""
    import responses
    
    with responses.RequestsMock() as rsps:
        rsps.add(
            responses.GET,
            "https://api.github.com/users/octocat",
            json={"login": "octocat", "id": 1},
            status=200
        )
        yield rsps

def test_fetch_user_from_github(mock_github_api):
    response = requests.get("https://api.github.com/users/octocat")
    data = response.json()
    assert data["login"] == "octocat"
```

## Database Mocking

```python
import pytest
from unittest.mock import Mock, patch

@pytest.fixture
def mock_database():
    """Mock database connection."""
    mock_db = Mock()
    mock_db.execute.return_value = [
        (1, "Alice", "alice@example.com"),
        (2, "Bob", "bob@example.com")
    ]
    return mock_db

def test_fetch_users(mock_database):
    from source.lib.user_service import UserService
    
    service = UserService(mock_database)
    users = service.list_users()
    
    assert len(users) == 2
    assert users[0]["name"] == "Alice"
    mock_database.execute.assert_called_once()
```

## File I/O Mocking

```python
import pytest
from unittest.mock import mock_open, patch

@patch('builtins.open', new_callable=mock_open, read_data='file content')
def test_read_config_file(mock_file):
    from source.lib.config import load_config
    
    config = load_config("config.yaml")
    
    assert config == 'file content'
    mock_file.assert_called_with('config.yaml', 'r')
```

## Service Error Scenarios

```python
import pytest
from unittest.mock import patch
import requests

@patch('requests.get')
def test_api_timeout(mock_get):
    """Test handling of API timeout."""
    mock_get.side_effect = requests.Timeout("Request timed out")
    
    from source.lib.api_client import ApiClient
    client = ApiClient()
    
    with pytest.raises(ServiceUnavailableError):
        client.fetch_data()

@patch('requests.get')
def test_api_not_found(mock_get):
    """Test handling of 404 response."""
    mock_response = Mock()
    mock_response.status_code = 404
    mock_response.raise_for_status.side_effect = requests.HTTPError("404 Not Found")
    mock_get.return_value = mock_response
    
    from source.lib.api_client import ApiClient
    client = ApiClient()
    
    with pytest.raises(NotFoundError):
        client.fetch_user(999)
```

## Cache/Session Mocking

```python
import pytest
from unittest.mock import Mock, patch

@patch('redis.Redis')
def test_cached_user_lookup(mock_redis):
    """Test cache hit scenario."""
    mock_cache = Mock()
    mock_redis.return_value = mock_cache
    mock_cache.get.return_value = '{"id": 1, "name": "Alice"}'
    
    from source.lib.user_service import UserService
    service = UserService()
    
    user = service.get_user(1)
    assert user["name"] == "Alice"
    mock_cache.get.assert_called_once_with("user:1")
```
