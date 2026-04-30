# JWT Security Review

## What is working well

| Point | Verdict | Detail |
|---|---|---|
| **Expiration** | ✅ | 15 minutes — good value for an access token |
| **Identity** | ✅ | `create_access_token(str(user.id))` — standard usage |
| **Password hashing** | ✅ | `generate_password_hash` / `check_password_hash` (Werkzeug) |
| **Route protection** | ✅ | `@jwt_required()` on all `/tasks` endpoints |
| **OpenAPI security scheme** | ✅ | `BearerAuth` correctly declared in `API_SPEC_OPTIONS` |

---

## Issues detected

### 1. Hardcoded fallback secret key — High risk

**File**: `source/config/app_config.py`

```python
JWT_SECRET_KEY: str = os.environ.get(
    "JWT_SECRET_KEY", "dev-jwt-secret-change-in-production"
)
```

**Problem**: if `JWT_SECRET_KEY` is not set in production, the app runs with the secret `"dev-jwt-secret-change-in-production"` — known to anyone who reads the code. Anyone could forge a valid token.

**Fix**: no fallback in production — raise an exception at startup if the variable is missing:

```python
# In ProductionAppConfig only:
JWT_SECRET_KEY: str = os.environ["JWT_SECRET_KEY"]  # KeyError → crash at startup if missing
```

The fallback can stay in `DevelopmentAppConfig`.

---

### 2. Algorithm not explicitly configured — Medium risk

**File**: `source/config/flask_config.py`

The algorithm is never set. `flask-jwt-extended` defaults to `HS256` — acceptable — but relying on the implicit is risky:
- If the library changes its default in a future version, the behavior changes silently.
- The `none` algorithm (disabled in modern versions of PyJWT) is never explicitly rejected in config.

**Fix**: configure explicitly in `apply_jwt_config()`:

```python
config.JWT_ALGORITHM = "HS256"
```

---

### 3. No refresh token — Architectural limitation

15-minute expiration is a good value, but without a refresh token the user must log in again every 15 minutes. This is not a security problem but a design choice to confirm: is this intentional (stateless API, machine-to-machine usage) or should it be implemented?

---

### 4. No revocation — Classic JWT limitation

No blacklist mechanism. A stolen token remains valid until expiration (15 min). Acceptable for a first implementation, but should be documented as a known limitation.

---

## Summary

The overall pattern is good: `flask-jwt-extended` well integrated, correct expiration, protected routes. The only real security problem is the **hardcoded fallback secret key in production**. The implicit algorithm is a minor risk.

### Recommended actions

1. **Required**: remove the fallback from `ProductionAppConfig`, raise `KeyError` if `JWT_SECRET_KEY` is missing
2. **Recommended**: add `config.JWT_ALGORITHM = "HS256"` explicitly in `apply_jwt_config()`
3. **Optional**: decide whether a refresh token is needed or if the 401 every 15 min is acceptable
