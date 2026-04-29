# Database Testing Patterns

## In-Memory Database (SQLite)

```python
import pytest
from source.lib.database import Database

@pytest.fixture
def test_db():
    """Create in-memory SQLite database for tests."""
    db = Database(":memory:")
    db.create_schema()  # Create tables
    yield db
    db.close()

def test_user_persistence(test_db):
    """Test storing and retrieving users."""
    test_db.users.insert({"id": 1, "name": "Alice"})
    
    user = test_db.users.fetch_one(id=1)
    assert user["name"] == "Alice"
```

## Database Fixtures with Rollback

```python
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

@pytest.fixture(scope="function")
def db_session():
    """Transaction-scoped session that rolls back after test."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    connection = engine.connect()
    transaction = connection.begin()
    
    session = Session(bind=connection)
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()

def test_with_db_rollback(db_session):
    """Each test starts with clean database."""
    user = User(name="Bob")
    db_session.add(user)
    db_session.commit()
    
    assert db_session.query(User).count() == 1
```

## Parametrized Database Tests

```python
import pytest
from source.lib.models import User
from source.lib.repositories import UserRepository

@pytest.mark.parametrize("name,email", [
    ("Alice", "alice@example.com"),
    ("Bob", "bob@example.com"),
    ("Charlie", "charlie@example.com"),
])
def test_create_multiple_users(test_db, name, email):
    """Test creating different types of users."""
    repo = UserRepository(test_db)
    
    user = User(name=name, email=email)
    user_id = repo.create(user)
    
    retrieved = repo.get(user_id)
    assert retrieved.name == name
    assert retrieved.email == email
```

## Testing Transactions

```python
import pytest
from source.lib.order_service import OrderService

def test_order_rollback_on_error(test_db):
    """Test transaction rollback when error occurs."""
    service = OrderService(test_db)
    
    # Create order
    try:
        service.create_order(user_id=1, items=[], amount=-100.00)  # Invalid
    except ValueError:
        pass
    
    # Order should not exist (transaction rolled back)
    orders = test_db.query(Order).all()
    assert len(orders) == 0
```

## Migration Testing

```python
import pytest
from alembic.command import upgrade, downgrade
from alembic.config import Config

@pytest.fixture(scope="function")
def migrated_db():
    """Test database with all migrations applied."""
    config = Config("alembic.ini")
    alembic_dir = "alembic"
    
    # Create database schema
    db = Database(":memory:")
    
    # Apply migrations
    upgrade(config, "head")
    
    yield db

def test_user_schema_after_migration(migrated_db):
    """Verify user table exists with correct columns."""
    columns = migrated_db.get_columns("users")
    assert "id" in columns
    assert "email" in columns
```
