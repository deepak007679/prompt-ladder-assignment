# Production Backend Feature Prompt Template (Stranger-Ready)

This prompt template was engineered through empirical testing across the Prompt Ladder. It is designed so that any backend engineer on the team can copy, fill in the parameter brackets, and get production-grade, modular, verified code without author guidance.

---

## 📋 The Template

```markdown
Role: Senior Backend Infrastructure Engineer
Objective: Implement [FEATURE_NAME] for our [DOMAIN_TYPE] backend service.

Context & Environment:
- Language & Runtime: Python 3.11+
- Framework: FastAPI (modern asynchronous patterns, dependency injection)
- Persistence: PostgreSQL via SQLAlchemy 2.0 (asyncpg, DeclarativeBase, Mapped types)
- Cache & Session Store: Redis 7.0 (redis.asyncio)
- Secret Management: Configuration via pydantic-settings BaseSettings reading environment variables

Requirements & Business Logic:
1. [REQUIREMENT_1 - e.g., User registration with email uniqueness checks and salted bcrypt password hashing]
2. [REQUIREMENT_2 - e.g., JWT access token issuance (15 min exp) and refresh token rotation with Redis blocklist tracking]
3. [REQUIREMENT_3 - e.g., Password reset token generation with cryptographically secure single-use tokens expiring in 1 hour]
4. [REQUIREMENT_4 - e.g., Token revocation endpoint on logout that blacklists token JTI in Redis]

Specified Output Format:
Organize the implementation across clean, modular files with explicit markdown file headers:
1. `app/schemas/[MODULE].py`: Strict Pydantic v2 schemas for all Request, Response, and Event models with validation constraints.
2. `app/core/[UTILITY].py`: Reusable domain logic, security routines, hashing helpers, or client connection singletons.
3. `app/api/v1/[MODULE].py`: FastAPI APIRouter endpoints using `Depends` for database sessions, caching, and current user context.
4. `tests/test_[MODULE].py`: Asynchronous test suite using `pytest-asyncio` and `httpx.AsyncClient`.

Verification & Quality Criteria:
- Do not omit implementation details with `# TODO: implement later` or pass placeholder blocks.
- Ensure all route exceptions raise typed `HTTPException` with RFC-7807 compliant error details.
- All database transactions must commit or rollback cleanly within async session context managers.
- The test suite in `tests/test_[MODULE].py` must include:
  a. Happy-path integration test asserting 200/201 HTTP status and response payload validation.
  b. Negative edge case testing invalid input / authentication failure returning 400/401/403.
  c. Failure recovery test simulating database or cache disconnection or state expiration.
```

---

## 🛠️ Concrete Example: User Authentication & Session Revocation

Below is an example of the template populated for an enterprise authentication microservice:

```markdown
Role: Senior Backend Infrastructure Engineer
Objective: Implement User Authentication and Session Token Generation for our B2B SaaS platform.

Context & Environment:
- Language & Runtime: Python 3.11
- Framework: FastAPI 0.110+
- Persistence: PostgreSQL via SQLAlchemy 2.0 with asyncpg driver
- Cache: Redis 7.0 with redis.asyncio client
- Secret Management: pydantic-settings BaseSettings reading APP_SECRET_KEY, DATABASE_URL, REDIS_URL

Requirements & Business Logic:
1. User registration validates email format and password strength (min 8 chars, 1 digit, 1 special char). Passwords hashed using bcrypt.
2. Login accepts email + password, verifies credentials, and issues an HMAC-SHA256 JWT access token containing subject (user_id), email, and a unique `jti` uuid with 15-minute expiry.
3. Logout endpoint takes active Bearer token, extracts `jti`, and stores it in Redis with key `bl:<jti>` and TTL matching remaining token lifespan.
4. Protected endpoint dependency checks token validity and verifies `jti` is not in Redis blocklist.

Specified Output Format:
Organize the implementation across clean, modular files with explicit markdown file headers:
1. `app/schemas/auth.py`: Pydantic v2 schemas (UserRegisterRequest, UserLoginRequest, TokenResponse, UserProfileResponse).
2. `app/core/security.py`: Password hashing utilities (passlib[bcrypt]) and JWT create/decode functions (python-jose).
3. `app/api/v1/auth.py`: FastAPI APIRouter endpoints for /register, /login, /logout, and /me.
4. `tests/test_auth.py`: Asynchronous test suite using `pytest-asyncio` and `httpx.AsyncClient`.

Verification & Quality Criteria:
- No placeholder `# TODO` blocks; write complete executable logic.
- Return explicit HTTP 401 Unauthorized with detail message when credentials fail or token is revoked.
- Include pytest cases for:
  a. Valid registration and login returning JWT.
  b. Invalid password returning 401 Unauthorized.
  c. Expired token rejection.
  d. Revoked token (after logout) blocked by Redis check.
```
