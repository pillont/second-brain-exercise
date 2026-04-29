# Exercise: Building a Simple Task Management API

## Objective:
Design and implement a RESTful API for managing tasks. The API should allow users to create, retrieve, update, and delete tasks. Additionally, implement user authentication to secure the API.

## Requirements:

### Task Model:

Define a Task model with the following attributes:
* ID (auto-generated)
* Title
* Description
* Due Date
* Status (e.g., "Incomplete," "Complete")

### API Endpoints:

Implement the following RESTful endpoints using a framework of your choice (e.g., Flask, Express, Django):
* POST /tasks: Create a new task.
* GET /tasks: Retrieve a list of all tasks.
* GET /tasks/{id}: Retrieve details of a specific task by ID.
* PUT /tasks/{id}: Update the details of a specific task.
* DELETE /tasks/{id}: Delete a specific task.

### User Authentication:

* Implement a simple user authentication system using JWT.
* Create endpoints for user registration and login.
* Ensure that task-related endpoints are protected and can only be accessed by authenticated users.

### Validation and Error Handling:

* Implement proper input validation for task creation and update.
* Handle errors gracefully and return meaningful error messages with appropriate HTTP status codes.

### Testing:

* Write unit tests for at least one endpoint.
* Include tests for both successful and unsuccessful scenarios.

## Additional Considerations (Optional):

* Implement pagination for the list of tasks to manage large datasets.
* Add filtering options to retrieve tasks based on status, due date, etc.
* Include sorting options for the list of tasks.
* Use a database of your choice (e.g., SQLite, PostgreSQL) to persist task and user data.

## Submission:
Share the codebase along with a README file explaining how to set up and run the application. Include details on API usage, authentication, and any additional features implemented.

## Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Installation

1. **Set up virtual environment** (optional but recommended):
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

### Running the API

**Option 1 — VS Code (recommended)**: press **F5** (Run & Debug). The server starts and the Swagger UI opens automatically in the browser.

**Option 2 — terminal**: always run from the project root using `-m` (not `python source/app.py`):
```bash
.venv/bin/python -m source.app
```

The API runs on **http://127.0.0.1:5001** (port 5001, not 5000 — macOS AirPlay Receiver occupies port 5000).

Swagger UI: **http://127.0.0.1:5001/swagger-ui**

### Testing the API

**Example 1: Using curl**
```bash
curl http://127.0.0.1:5001/hello
```

Expected response:
```json
{
  "id": 1,
  "message": "Hello from API!"
}
```

### Project Structure

The project follows a **5-layer MVC architecture** for clean separation of concerns:

```
source/
├── __init__.py           # Flask app factory (create_app function)
├── app.py                # Application entry point
├── config.py             # Configuration by environment
├── container.py          # Dependency injection container
├── controllers/          # HTTP endpoints and request handling
├── services/             # Business logic and validation
├── repositories/         # Data access layer (future)
├── models/               # Domain entities
├── utils/                # Helper functions and decorators
└── tests/                # Unit and integration tests
```

For detailed architecture documentation, see [source/architecture.md](source/architecture.md)

## Implementation Decisions for Future Development

### 1. Dependency Injection
- **Library**: `dependency-injector` for professional-grade service management
- **Pattern**: Services are singleton instances registered in container
- **Injection**: Use `@inject` decorator in controllers with `Provide[Container.service_name]`
- **Never**: Don't use static methods or manual instantiation

### 2. Service Definition
- Services must be **instance methods** (not static)
- Services can receive dependencies via constructor (injected by container)
- Services contain pure business logic, not HTTP handling

Example service pattern:
```python
class MyService:
    def __init__(self, repository):
        self.repository = repository
    
    def do_something(self, param):
        return self.repository.query(param)
```

### 3. Container Registration
All services must be registered in `source/container.py`:
```python
class Container(containers.DeclarativeContainer):
    my_repository = providers.Singleton(MyRepository)
    my_service = providers.Singleton(MyService, repository=my_repository)
```

And wired in `source/__init__.py`:
```python
container.wire(modules=['source.controllers.my_controller'])
```

### 4. Controller Endpoints
Endpoints must use `@inject` decorator:
```python
@inject
def my_endpoint(my_service=Provide[Container.my_service]):
    return my_service.do_something()
```

### 5. Code Style
- **No docstrings**: Only inline comments if logic is not obvious
- **Type hints**: All function parameters and returns must have types
- **Logging**: Use logger.info/warning/error for tracking
- **Errors**: Return JSON errors with appropriate HTTP status codes

---

For detailed architecture documentation, see [source/architecture.md](source/architecture.md)

---

Note:
Feel free to use any programming language, framework, or additional libraries that you are comfortable with. The exercise is designed to assess your skills in API design, database interaction, user authentication, and testing.