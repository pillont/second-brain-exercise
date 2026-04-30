---
name: python-clean-code-solid
description: "Write clean, maintainable Python code following SOLID principles and best practices. Use when: designing classes/functions, refactoring code, improving readability, reducing technical debt, applying design patterns, or ensuring code follows SRP, OCP, LSP, ISP, DIP."
argument-hint: "Optional: file path or class name to review/refactor"
---

# Clean Code & SOLID Principles

## When to Use

- Design new classes or functions
- Refactor existing code for readability
- Reduce code duplication (DRY principle)
- Improve testability and maintainability
- Decouple components and reduce dependencies
- Apply design patterns appropriately
- Review code for adherence to standards

## SOLID Principles

### 1. Single Responsibility Principle (SRP)

**Definition**: A class or function should have only one reason to change.

❌ **Bad**: Class does too much
```python
class UserManager:
    def create_user(self, name: str, email: str) -> User:
        user = User(name, email)
        self.send_welcome_email(user)  # Email logic mixed in
        self.log_activity(f"Created user {name}")  # Logging mixed in
        return user
    
    def send_welcome_email(self, user: User) -> None:
        # Email implementation
        pass
    
    def log_activity(self, message: str) -> None:
        # Logging implementation
        pass
```

✅ **Good**: Separated concerns
```python
class UserRepository:
    """Only manages user persistence."""
    def create(self, name: str, email: str) -> User:
        return User(name, email)

class EmailService:
    """Only sends emails."""
    def send_welcome_email(self, user: User) -> None:
        # Email implementation
        pass

class Logger:
    """Only logs."""
    def log_activity(self, message: str) -> None:
        # Logging implementation
        pass

class UserManager:
    """Coordinates user creation workflow."""
    def __init__(self, repo: UserRepository, email: EmailService, logger: Logger):
        self.repo = repo
        self.email = email
        self.logger = logger
    
    def create_user(self, name: str, email: str) -> User:
        user = self.repo.create(name, email)
        self.email.send_welcome_email(user)
        self.logger.log_activity(f"Created user {name}")
        return user
```

### 2. Open/Closed Principle (OCP)

**Definition**: Classes should be open for extension, closed for modification.

❌ **Bad**: Must modify class for new features
```python
class PaymentProcessor:
    def process(self, method: str, amount: float) -> bool:
        if method == "credit_card":
            return self.process_credit_card(amount)
        elif method == "paypal":
            return self.process_paypal(amount)
        elif method == "bitcoin":  # New method requires code change
            return self.process_bitcoin(amount)
        return False
```

✅ **Good**: Extend without modifying
```python
from abc import ABC, abstractmethod

class PaymentMethod(ABC):
    @abstractmethod
    def process(self, amount: float) -> bool:
        pass

class CreditCard(PaymentMethod):
    def process(self, amount: float) -> bool:
        # Credit card implementation
        return True

class PayPal(PaymentMethod):
    def process(self, amount: float) -> bool:
        # PayPal implementation
        return True

class Bitcoin(PaymentMethod):  # New method, no existing code changed
    def process(self, amount: float) -> bool:
        # Bitcoin implementation
        return True

class PaymentProcessor:
    def process(self, method: PaymentMethod, amount: float) -> bool:
        return method.process(amount)  # All methods work transparently
```

### 3. Liskov Substitution Principle (LSP)

**Definition**: Subtypes must be substitutable for their base types without breaking functionality.

❌ **Bad**: Subtype breaks contract
```python
class Bird:
    def fly(self) -> str:
        return "Flying..."

class Penguin(Bird):
    def fly(self) -> str:
        raise NotImplementedError("Penguins cannot fly")

def make_bird_fly(bird: Bird) -> None:
    print(bird.fly())  # Works for Bird, fails for Penguin!
```

✅ **Good**: Subtypes honor contract
```python
class Animal:
    def move(self) -> str:
        pass

class Bird(Animal):
    def move(self) -> str:
        return "Flying..."

class Penguin(Animal):
    def move(self) -> str:
        return "Waddling..."

def make_animal_move(animal: Animal) -> None:
    print(animal.move())  # Works for all animals
```

### 4. Interface Segregation Principle (ISP)

**Definition**: Clients should depend on interfaces specific to their needs, not broad ones.

❌ **Bad**: Broad interface forces unused methods
```python
class Worker(ABC):
    @abstractmethod
    def work(self) -> None:
        pass
    
    @abstractmethod
    def manage_team(self) -> None:
        pass

class Developer(Worker):
    def work(self) -> None:
        print("Writing code...")
    
    def manage_team(self) -> None:
        raise NotImplementedError("Developers don't manage")  # Forced!
```

✅ **Good**: Segregated interfaces
```python
class Worker(ABC):
    @abstractmethod
    def work(self) -> None:
        pass

class TeamManager(ABC):
    @abstractmethod
    def manage_team(self) -> None:
        pass

class Developer(Worker):
    def work(self) -> None:
        print("Writing code...")

class Lead(Worker, TeamManager):
    def work(self) -> None:
        print("Writing code...")
    
    def manage_team(self) -> None:
        print("Managing team...")
```

### 5. Dependency Inversion Principle (DIP)

**Definition**: Depend on abstractions, not concrete implementations.

❌ **Bad**: Depends on concrete class
```python
class EmailSender:
    def send(self, email: str) -> None:
        # Send email implementation
        pass

class UserService:
    def __init__(self):
        self.email = EmailSender()  # Concrete dependency
    
    def notify_user(self, email: str) -> None:
        self.email.send(email)  # Tightly coupled
```

✅ **Good**: Depends on abstraction
```python
from abc import ABC, abstractmethod

class Notifier(ABC):
    @abstractmethod
    def notify(self, recipient: str) -> None:
        pass

class EmailSender(Notifier):
    def notify(self, recipient: str) -> None:
        # Send email implementation
        pass

class SMSSender(Notifier):
    def notify(self, recipient: str) -> None:
        # Send SMS implementation
        pass

class UserService:
    def __init__(self, notifier: Notifier):
        self.notifier = notifier  # Abstract dependency (injected)
    
    def notify_user(self, recipient: str) -> None:
        self.notifier.notify(recipient)  # Works with any Notifier
```

## Clean Code Best Practices

### Naming Conventions
```python
# ❌ Bad
def d(x: int, y: int) -> int:
    return x + y

# ✅ Good
def calculate_total(base_price: float, tax_amount: float) -> float:
    return base_price + tax_amount
```

### Function Length & Complexity
```python
# ❌ Bad: 50 lines, multiple responsibilities
def process_payment_and_send_receipt(user, amount):
    # Validate payment...
    # Process payment...
    # Save transaction...
    # Generate receipt HTML...
    # Send email...
    pass

# ✅ Good: Extract into single-purpose functions
def process_payment(user: User, amount: float) -> Transaction:
    return self.payment_processor.process(user, amount)

def send_receipt(user: User, transaction: Transaction) -> None:
    receipt = self.receipt_generator.generate(transaction)
    self.email.send(receipt)
```

### Comments & Documentation
```python
# ❌ Bad: Obvious comments clutter code
x = 5  # Set x to 5

# ✅ Good: Document non-obvious logic
max_retry_attempts = 5  # Max attempts before circuit breaker opens

# ✅ Use docstrings
def calculate_compound_interest(principal: float, rate: float, time: float) -> float:
    """Calculate compound interest using A = P(1 + r/n)^(nt).
    
    Args:
        principal: Initial amount in dollars
        rate: Annual interest rate (0.05 for 5%)
        time: Time in years
    
    Returns:
        Total amount after compound interest
    """
    return principal * (1 + rate) ** time
```

### Error Handling
```python
# ❌ Bad: Generic exception
try:
    result = dangerous_operation()
except Exception:
    print("Error")

# ✅ Good: Specific exceptions with context
try:
    result = dangerous_operation()
except TimeoutError:
    logger.error(f"Operation timed out after {timeout_seconds}s")
    raise ServiceError("Service unavailable") from None
except ValueError as e:
    logger.error(f"Invalid input: {e}")
    raise
```

## Refactoring Checklist

- [ ] Each class/function has single responsibility
- [ ] No duplication (DRY principle)
- [ ] Names clearly express intent
- [ ] Functions are short (<20 lines)
- [ ] Parameters are minimal (<3 parameters)
- [ ] Return types are clear and typed
- [ ] Error conditions are handled
- [ ] Code is testable (dependencies injectable)
- [ ] All tests pass
- [ ] No commented-out code

## References

- [Clean Code by Robert C. Martin](./python-clean-code-solid-references/clean-code-book.md)
- [SOLID Principles explained](./python-clean-code-solid-references/solid-explained.md)
- [Python design patterns](./python-clean-code-solid-references/design-patterns.md)
- [Code smells and refactoring](./python-clean-code-solid-references/code-smells.md)
- [Anti-patterns to avoid](./python-clean-code-solid-references/antipatterns.md)

## Tools & Linters

- **pylint**: Check for code smells and issues
  ```bash
  python -m pylint source/lib --disable=C0111
  ```
- **radon**: Measure code complexity
  ```bash
  python -m radon cc source/lib -a
  ```
- **mypy**: Static type checking (see [python-typing skill](./python-typing.md))
