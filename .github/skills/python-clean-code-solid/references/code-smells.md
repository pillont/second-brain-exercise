# Code Smells & Refactoring

## Common Code Smells

### 1. Long Method

**Problem**: Method does too much

```python
# ❌ Bad: 50+ lines
def process_order(order):
    # Validate order
    for item in order.items:
        if item.price < 0:
            raise ValueError()
    
    # Calculate totals
    subtotal = sum(i.price for i in order.items)
    tax = subtotal * 0.1
    total = subtotal + tax
    
    # Save to database
    db.orders.insert(...)
    
    # Send notification
    email.send(...)
    
    # Update inventory
    inventory.update(...)
    
    return total
```

**Solution**: Extract smaller functions

```python
# ✅ Good: Each function has single responsibility
def validate_order(order):
    for item in order.items:
        if item.price < 0:
            raise ValueError()

def calculate_total(order):
    subtotal = sum(i.price for i in order.items)
    return subtotal * 1.10  # Include tax

def process_order(order):
    validate_order(order)
    total = calculate_total(order)
    save_order(order)
    notify_customer(order)
    update_inventory(order)
    return total
```

### 2. Duplicate Code

**Problem**: Same code in multiple places

```python
# ❌ Bad: Duplication
class UserService:
    def create_admin(self, email):
        if not email or "@" not in email:
            raise ValueError("Invalid email")
        return User(email, role="admin")
    
    def create_user(self, email):
        if not email or "@" not in email:
            raise ValueError("Invalid email")
        return User(email, role="user")

# ✅ Good: Extracted validation
def validate_email(email):
    if not email or "@" not in email:
        raise ValueError("Invalid email")

class UserService:
    def create_admin(self, email):
        validate_email(email)
        return User(email, role="admin")
    
    def create_user(self, email):
        validate_email(email)
        return User(email, role="user")
```

### 3. Long Parameter List

**Problem**: Function has too many parameters

```python
# ❌ Bad: 7 parameters!
def create_report(user_id, start_date, end_date, filters, 
                  sort_by, include_totals, export_format):
    pass

# ✅ Good: Group into objects
class ReportRequest:
    def __init__(self, user_id, start_date, end_date):
        self.user_id = user_id
        self.start_date = start_date
        self.end_date = end_date
        self.filters = []
        self.sort_by = None
        self.include_totals = False
        self.export_format = "pdf"

def create_report(request: ReportRequest):
    pass
```

### 4. God Object

**Problem**: Class does everything

```python
# ❌ Bad: Does too much
class User:
    def validate(self): pass
    def save_to_db(self): pass
    def send_email(self): pass
    def log_activity(self): pass
    def authenticate(self): pass

# ✅ Good: Separated concerns
class User:
    name: str
    email: str

class UserValidator:
    def validate(user: User): pass

class UserRepository:
    def save(user: User): pass

class EmailService:
    def send(user: User): pass
```

### 5. Dead Code

**Problem**: Unreachable or unused code

```python
# ❌ Bad: Dead code
def get_user(user_id):
    return User.objects.get(id=user_id)
    return None  # Never reached

def format_name(first, last):
    return f"{first} {last}"
    # Commented out old code
    # old_format = first + " " + last
    # return old_format

# ✅ Good: Remove unused code
def get_user(user_id):
    return User.objects.get(id=user_id)

def format_name(first, last):
    return f"{first} {last}"
```

## Refactoring Techniques

### Extract Method

```python
# Before
def calculate_price(items):
    subtotal = sum(i.price for i in items)
    tax = subtotal * 0.1
    discount = subtotal * 0.05 if subtotal > 100 else 0
    return subtotal + tax - discount

# After
def calculate_price(items):
    subtotal = calculate_subtotal(items)
    tax = calculate_tax(subtotal)
    discount = calculate_discount(subtotal)
    return subtotal + tax - discount

def calculate_subtotal(items):
    return sum(i.price for i in items)

def calculate_tax(subtotal):
    return subtotal * 0.1

def calculate_discount(subtotal):
    return subtotal * 0.05 if subtotal > 100 else 0
```

### Move Method

```python
# Before: Method in wrong class
class User:
    def calculate_age(self):
        from datetime import date
        today = date.today()
        return today.year - self.birth_year

# After: Move to DateUtils
class DateUtils:
    @staticmethod
    def calculate_age(birth_year):
        from datetime import date
        today = date.today()
        return today.year - birth_year

class User:
    def get_age(self):
        return DateUtils.calculate_age(self.birth_year)
```

### Replace Temp with Query

```python
# Before
def get_price(order):
    base_price = order.quantity * order.item_price
    if base_price > 1000:
        return base_price * 0.95
    else:
        return base_price

# After
def get_price(order):
    return self.apply_discount(order.base_price())

def apply_discount(base_price):
    return base_price * 0.95 if base_price > 1000 else base_price
```
