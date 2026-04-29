# Integration Testing Guide

## When to Use Integration Tests

Integration tests verify multiple components work together:
- Component + Database
- Component + External API
- Component A + Component B
- Workflow across multiple modules

## Integration Test Pyramid

```
          /\          Unit Tests (70%)
         /  \         - Fast
        /    \        - Isolated
       /______\
      /\      /\      Integration Tests (20%)
     /  \    /  \     - Slower
    /____\__/____\    - Component interaction
   /\  /\  /\  /\     E2E Tests (10%)
  /  \/  \/  \/  \    - Slowest
 /________________\   - Full workflow
```

## Testing with External Services (Mocked)

```python
import pytest
from unittest.mock import patch, Mock

@pytest.fixture
def mock_external_api():
    """Mock external HTTP API."""
    with patch('requests.post') as mock:
        mock.return_value = Mock(
            status_code=200,
            json=lambda: {"status": "success", "id": 123}
        )
        yield mock

def test_user_registration_flow(mock_external_api):
    """Test registration with mocked payment API."""
    from source.lib.user_service import UserService
    
    service = UserService()
    user = service.register(
        email="user@example.com",
        plan="premium"
    )
    
    # API was called
    mock_external_api.assert_called_once()
    # User registered successfully
    assert user.email == "user@example.com"
    assert user.plan == "premium"
```

## Database Integration Tests

```python
import pytest
from source.lib.models import User
from source.lib.database import Database

@pytest.fixture
def test_db():
    """In-memory SQLite database for testing."""
    db = Database(":memory:")
    db.create_tables()
    yield db
    db.close()

class TestUserRepository:
    def test_create_retrieve_update_delete(self, test_db):
        """Full CRUD operation test."""
        from source.lib.repositories import UserRepository
        
        repo = UserRepository(test_db)
        
        # CREATE
        user = User(name="Alice", email="alice@example.com")
        user_id = repo.create(user)
        assert user_id > 0
        
        # RETRIEVE
        retrieved = repo.get(user_id)
        assert retrieved.name == "Alice"
        
        # UPDATE
        retrieved.email = "alice_new@example.com"
        repo.update(retrieved)
        
        # VERIFY UPDATE
        updated = repo.get(user_id)
        assert updated.email == "alice_new@example.com"
        
        # DELETE
        repo.delete(user_id)
        assert repo.get(user_id) is None
```

## Multi-Component Workflow Tests

```python
import pytest
from unittest.mock import patch

@pytest.fixture
def services():
    """Provide all services for integration test."""
    from source.lib.order_service import OrderService
    from source.lib.inventory_service import InventoryService
    from source.lib.payment_service import PaymentService
    
    return {
        'order': OrderService(),
        'inventory': InventoryService(),
        'payment': PaymentService()
    }

def test_order_to_shipment_workflow(services):
    """Test complete order workflow: create → pay → ship."""
    # Create order
    order = services['order'].create(user_id=1, items=["item1", "item2"])
    assert order.status == "created"
    
    # Check inventory
    in_stock = services['inventory'].check_availability(order.items)
    assert in_stock is True
    
    # Process payment
    payment = services['payment'].process(order.id, amount=100.00)
    assert payment.status == "approved"
    
    # Mark order as shipped
    order = services['order'].update_status(order.id, "shipped")
    assert order.status == "shipped"
```

## Tools for Integration Testing

- **pytest-mock**: Simplified mocking
- **responses**: Mock HTTP requests
- **pytest-postgresql**: Test with real PostgreSQL
- **testcontainers**: Docker containers for services
- **fakeredis**: Mock Redis
