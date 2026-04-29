# SOLID Principles Explained

## Single Responsibility Principle (SRP)

**One class = One reason to change**

```python
# ❌ Bad: Class responsible for user data AND persistence
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email
    
    def validate(self):
        if not self.email:
            raise ValueError("Email required")
    
    def save_to_database(self):
        # SQL code mixed in
        pass

# ✅ Good: Separated concerns
class User:
    """Only manages user data."""
    name: str
    email: str
    
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email

class UserValidator:
    """Only validates user data."""
    def validate(self, user: User) -> bool:
        return bool(user.email)

class UserRepository:
    """Only handles persistence."""
    def save(self, user: User) -> None:
        # Database code
        pass
```

## Open/Closed Principle (OCP)

**Open for extension, closed for modification**

```python
# ❌ Bad: Must modify for each new payment type
class PaymentProcessor:
    def process(self, payment_type: str, amount: float):
        if payment_type == "credit_card":
            # Process credit card
            pass
        elif payment_type == "paypal":
            # Process PayPal
            pass
        # New type? Modify this class!

# ✅ Good: Extend by creating new classes
from abc import ABC, abstractmethod

class PaymentMethod(ABC):
    @abstractmethod
    def process(self, amount: float) -> bool:
        pass

class CreditCardPayment(PaymentMethod):
    def process(self, amount: float) -> bool:
        pass

class PayPalPayment(PaymentMethod):
    def process(self, amount: float) -> bool:
        pass

# New payment type? Just add a new class!
class BitcoinPayment(PaymentMethod):
    def process(self, amount: float) -> bool:
        pass
```

## Liskov Substitution Principle (LSP)

**Subtypes must be substitutable for base types**

```python
# ❌ Bad: Subtype breaks the contract
class Bird:
    def fly(self) -> str:
        return "Flying"

class Penguin(Bird):
    def fly(self) -> str:
        raise NotImplementedError("Penguins can't fly")

def operate_bird(bird: Bird):
    print(bird.fly())  # Fails for Penguin!

# ✅ Good: All subtypes honor the contract
class Animal:
    def move(self) -> str:
        pass

class Dog(Animal):
    def move(self) -> str:
        return "Running"

class Bird(Animal):
    def move(self) -> str:
        return "Flying"

class Penguin(Animal):
    def move(self) -> str:
        return "Waddling"

def operate_animal(animal: Animal):
    print(animal.move())  # Works for all animals!
```

## Interface Segregation Principle (ISP)

**Clients shouldn't depend on interfaces they don't use**

```python
# ❌ Bad: Interface forces unrelated methods
class Worker(ABC):
    @abstractmethod
    def work(self): pass
    
    @abstractmethod
    def take_break(self): pass
    
    @abstractmethod
    def manage_team(self): pass

class Developer(Worker):
    def work(self): pass
    def take_break(self): pass
    def manage_team(self): 
        raise NotImplementedError()  # Forced but not needed!

# ✅ Good: Segregated interfaces
class Worker(ABC):
    @abstractmethod
    def work(self): pass

class Relatable(ABC):
    @abstractmethod
    def take_break(self): pass

class Manager(ABC):
    @abstractmethod
    def manage_team(self): pass

class Developer(Worker, Relatable):
    def work(self): pass
    def take_break(self): pass

class TeamLead(Worker, Relatable, Manager):
    def work(self): pass
    def take_break(self): pass
    def manage_team(self): pass
```

## Dependency Inversion Principle (DIP)

**Depend on abstractions, not concretions**

```python
# ❌ Bad: Depends on concrete class
class Logger:
    def log(self, msg: str): pass

class UserService:
    def __init__(self):
        self.logger = Logger()  # Concrete dependency!
    
    def create_user(self, name: str):
        self.logger.log(f"Creating {name}")

# ✅ Good: Depends on abstraction
from abc import ABC, abstractmethod

class LoggerInterface(ABC):
    @abstractmethod
    def log(self, msg: str): pass

class Logger(LoggerInterface):
    def log(self, msg: str): pass

class FileLogger(LoggerInterface):
    def log(self, msg: str): pass

class UserService:
    def __init__(self, logger: LoggerInterface):
        self.logger = logger  # Injected abstraction
    
    def create_user(self, name: str):
        self.logger.log(f"Creating {name}")
```
