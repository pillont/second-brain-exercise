# Testing Conventions

## Filter feature — required test cases per layer

When adding filters to a `GET /resource/` endpoint, cover all cases at every layer.

### 1. Model filter class (`test_models/test_<resource>_filters.py`)

- `apply` with no filter → returns all elements
- each filter field in isolation
- text fields: case-insensitive contains
- date fields: `from` inclusive, `to` inclusive, combined range
- multiple filters combined
- no element matches → empty

### 2. Repository (`test_repositories/test_fake_<resource>_repository.py`)

- each filter field in isolation (returns matching, excludes non-matching)
- text: case-insensitive
- combined filters
- filters applied **before** pagination — e.g. 2 Incomplete + 1 Complete, `page_size=1` + `status=Incomplete` → 1 element, `has_next=True`
- empty `Filters()` object → returns everything

### 3. Service (`test_services/test_get_all_<resource>_service.py`)

- `get_all(filters=x)` → repository called with correct `filters` (`assert_called_once_with`)
- `get_all(cursor=x, page_size=y)` → pagination params forwarded
- `get_all(filters=x, cursor=y, page_size=z)` → all three params forwarded together

### 4. Integration (`test_integration/test_<resource>_controller.py`)

- each filter field in isolation
- text fields: pass value in uppercase to verify case-insensitivity
- date range (from + to together)
- combined filters (e.g. status + title)
- filter + pagination → verify `has_next`
- **filter returns empty list** → assert `elements == []` and `has_next == false`
- **filter returns multiple elements** → assert count and `has_next`
- invalid enum value → 422
