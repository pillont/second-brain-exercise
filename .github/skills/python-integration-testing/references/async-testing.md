# Async Testing with pytest-asyncio

## Installation

```bash
python -m pip install pytest-asyncio
```

## Basic Async Tests

```python
import pytest
import asyncio

@pytest.mark.asyncio
async def test_async_function():
    """Test async function."""
    result = await some_async_function()
    assert result == expected

@pytest.mark.asyncio
async def test_async_with_multiple_awaits():
    """Test multiple async operations."""
    result1 = await fetch_data(1)
    result2 = await fetch_data(2)
    
    assert result1 is not None
    assert result2 is not None
```

## Async Context and Setup

```python
import pytest
from asyncio import Event

@pytest.fixture
async def async_client():
    """Fixture for async HTTP client."""
    client = AsyncClient()
    await client.connect()
    yield client
    await client.disconnect()

@pytest.mark.asyncio
async def test_with_async_fixture(async_client):
    response = await async_client.get("/api/users")
    assert response.status == 200
```

## Async Task Testing

```python
import pytest
import asyncio

@pytest.mark.asyncio
async def test_concurrent_tasks():
    """Test multiple concurrent async tasks."""
    tasks = [
        fetch_user(1),
        fetch_user(2),
        fetch_user(3),
    ]
    
    results = await asyncio.gather(*tasks)
    assert len(results) == 3

@pytest.mark.asyncio
async def test_timeout_handling():
    """Test handling task timeout."""
    with pytest.raises(asyncio.TimeoutError):
        await asyncio.wait_for(slow_operation(), timeout=1)
```

## Mocking Async Functions

```python
import pytest
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_async_with_mock():
    """Mock async function."""
    with patch('aiohttp.ClientSession.get') as mock_get:
        mock_response = AsyncMock()
        mock_response.json = AsyncMock(return_value={"id": 1})
        mock_get.return_value = mock_response
        
        result = await fetch_api_data()
        assert result["id"] == 1

@pytest.mark.asyncio
async def test_mock_side_effect():
    """Mock with side effect."""
    mock_func = AsyncMock()
    mock_func.side_effect = [1, 2, 3]
    
    assert await mock_func() == 1
    assert await mock_func() == 2
    assert await mock_func() == 3
```

## pytest Configuration for Async

Add to `pytest.ini`:

```ini
[pytest]
asyncio_mode = auto
markers =
    asyncio: marks tests as async
```

## Event Loop Management

```python
import pytest

@pytest.fixture(scope="session")
def event_loop():
    """Create custom event loop for all tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
```
