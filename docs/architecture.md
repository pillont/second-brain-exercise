# Architecture

5-layer MVC — each layer has one responsibility, flow is always downward.

## Layers

```
source/
├── config/        (AppConfig TypedDict, FlaskConfig subclasses)
├── models/        (domain models, StrEnum, error types)
├── repositories/  (ABCs + in-memory fakes + SQLAlchemy implementations)
├── services/      (one service class per operation)
├── controllers/   (blueprints, schemas, DTO, mappers, utils)
└── tests/         (unit/ + integration/)
```

## Data Flow

**POST /tasks — create a task**:
```
1. HTTP POST /tasks/ with JSON body
   ↓
2. [Controller] create_task()
   - flask-smorest deserializes body via TaskDataSchema → TaskDataDTO
   - Calls to_task_data() mapper → TaskData domain object
   - Calls CreateTaskService.create_task(task_data)
   ↓
3. [Service] CreateTaskService.create_task()
   - Delegates to CreateTaskRepository.create(task_data)
   - Returns Task model
   ↓
4. [Repository] create()
   - Assigns auto-incremented id, sets status=INCOMPLETE
   - Returns Task
   ↓
5. [Controller] calls to_task_dto(task) → TaskDTO with _links
   - flask-smorest serializes via TaskSchema → JSON
   - Returns HTTP 201
```

**DELETE /tasks/{id} — delete a task**:
```
1. HTTP DELETE /tasks/42
   ↓
2. [Controller] delete_task(id=42)
   - Calls DeleteTaskService.delete_task(42)
   ↓
3. [Service] DeleteTaskService.delete_task()
   - Delegates to DeleteTaskRepository.delete_task(42)
   ↓
4. [Repository] delete_task()
   - Finds task by id (raises NotFoundError if missing → 404)
   - Removes task from store
   ↓
5. [Controller] Returns HTTP 204 (no body)
```

## See also

- [project-structure](.claude/commands/project-structure.md) — full annotated file tree
- [hateoas](.claude/commands/hateoas.md) — DTO, mappers, `_links`
- [dependency-injection](.claude/commands/dependency-injection.md) — container wiring
