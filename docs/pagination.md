# Pagination & Filtering Strategy

## Cursor-based vs Offset-based Pagination

Most basic APIs use **offset pagination** (`?page=2&size=10`). Its main drawback: if a record is inserted or deleted between two requests, the next page will return duplicate or skipped items.

This API uses **cursor-based pagination** instead. A cursor encodes the position of the last item seen, making each page request stable regardless of concurrent writes.

Reference: [Pagination Demystified — Three Layers You Shouldn't Mix Up](https://medium.com/@tpierrain/pagination-demystified-three-layers-you-shouldnt-mix-up-b5cca3b8e755)

## How the Cursor Works

The `TaskCursor` model holds two values:

- `sort_value` — the value of the sort field for the last item on the previous page
- `id` — the task ID, used as a tiebreaker when sort values are equal

The cursor is serialized as a base64-encoded JSON string and returned in the `_links.next` field of each list response. The client passes it back as the `cursor` query parameter.

```
GET /v1/tasks?sort_by=due_date&direction=asc&page_size=20
→ returns items + _links.next with an opaque cursor

GET /v1/tasks?sort_by=due_date&direction=asc&page_size=20&cursor=eyJ2IjogIjIwMjUtMDEtMDEiLCAiaWQiOiA0Mn0=
→ returns the next page, starting after the last seen item
```

The cursor is opaque to the client — its internal structure is irrelevant and can change without breaking the API contract.

## Sorting

The sort field and direction are query parameters:

| Parameter | Values | Default |
|-----------|--------|---------|
| `sort_by` | `id`, `title`, `due_date`, `status` | `id` |
| `direction` | `asc`, `desc` | `asc` |

The cursor encodes the value of the active sort field so the SQL query can efficiently seek past it using a `WHERE (sort_col, id) > (last_sort_value, last_id)` condition.

## Filtering

`GET /v1/tasks` accepts the following optional filter parameters:

| Parameter | Type | Description |
|-----------|------|-------------|
| `status` | `Incomplete` \| `Complete` | Filter by task status |
| `title` | `string` | Case-insensitive substring match on title |
| `due_date_from` | `date` (ISO 8601) | Tasks with due date on or after this date |
| `due_date_to` | `date` (ISO 8601) | Tasks with due date on or before this date |

Filters are applied before pagination. The cursor remains valid as long as the same filter parameters are used across pages.

## Database Indexes

The `tasks` table declares indexes on `title`, `due_date`, and `status` at the ORM level:

```python
title: Mapped[str] = mapped_column(String(255), index=True)
due_date: Mapped[date] = mapped_column(Date, index=True)
status: Mapped[str] = mapped_column(String(50), index=True)
```

These indexes ensure that filter and sort queries remain performant as the dataset grows, without requiring manual `CREATE INDEX` migrations.
