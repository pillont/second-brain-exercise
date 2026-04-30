# Python Design Patterns

## Creational Patterns

### 1. Singleton Pattern

Ensure a class has only one instance:

```python
class Database:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

# Usage
db1 = Database()
db2 = Database()
assert db1 is db2  # Same instance
```

### 2. Factory Pattern

Create objects without specifying exact classes:

```python
class PaymentFactory:
    @staticmethod
    def create(payment_type: str) -> PaymentMethod:
        if payment_type == "credit_card":
            return CreditCardPayment()
        elif payment_type == "paypal":
            return PayPalPayment()
        raise ValueError(f"Unknown type: {payment_type}")

# Usage
payment = PaymentFactory.create("credit_card")
```

## Structural Patterns

### 1. Adapter Pattern

Convert interface of one class to another:

```python
class OldAPIClient:
    def fetch_data(self): pass

class NewAPI:
    def get_data(self): pass

class APIAdapter(OldAPIClient):
    def __init__(self, new_api: NewAPI):
        self.api = new_api
    
    def fetch_data(self):
        return self.api.get_data()  # Adapt new interface
```

### 2. Decorator Pattern

Add behavior to objects dynamically:

```python
def timing_decorator(func):
    import time
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(f"Executed in {time.time() - start}s")
        return result
    return wrapper

@timing_decorator
def slow_operation():
    pass
```

## Behavioral Patterns

### 1. Strategy Pattern

Define algorithms in separate classes:

```python
class SortingStrategy:
    def sort(self, data): pass

class QuickSort(SortingStrategy):
    def sort(self, data):
        # QuickSort implementation
        pass

class MergeSort(SortingStrategy):
    def sort(self, data):
        # MergeSort implementation
        pass

class Sorter:
    def __init__(self, strategy: SortingStrategy):
        self.strategy = strategy
    
    def sort(self, data):
        return self.strategy.sort(data)
```

### 2. Observer Pattern

Notify multiple objects about state changes:

```python
class Observer(ABC):
    @abstractmethod
    def update(self, event): pass

class Subject:
    def __init__(self):
        self.observers = []
    
    def attach(self, observer: Observer):
        self.observers.append(observer)
    
    def notify(self, event):
        for observer in self.observers:
            observer.update(event)

class Listener(Observer):
    def update(self, event):
        print(f"Received event: {event}")
```

### 3. Command Pattern

Encapsulate requests as objects:

```python
class Command(ABC):
    @abstractmethod
    def execute(self): pass

class SaveCommand(Command):
    def __init__(self, document):
        self.document = document
    
    def execute(self):
        self.document.save()

class CommandQueue:
    def __init__(self):
        self.commands = []
    
    def enqueue(self, command: Command):
        self.commands.append(command)
    
    def execute_all(self):
        for cmd in self.commands:
            cmd.execute()
```
