# The Prompt Ladder: Systematic Layer-by-Layer Prompt Optimization

**Track:** Backend Engineering (Python / FastAPI / Distributed Systems)  
**Author:** Deepak (Backend Engineer)  
**Date:** October 2026  

---

## Overview

The gap between a lazy prompt and an engineered one is the cheapest performance upgrade in AI. Most engineers never experience this leap because they change five things at once and learn nothing about cause and effect. 

This document traces a six-stage **Prompt Ladder** for generating production-grade backend code. Starting with a genuinely weak and embarrassing baseline (`"Write backend code"`), each iteration introduces **exactly one named layer** targeting the most glaring weakness of the previous output.

---

## 🪜 Step 0: The Weak Baseline (Run 0)

### The Prompt
```text
Write backend code
```

### Representative Output Excerpt
```javascript
// Here is a simple backend server using Node.js and Express:
const express = require('express');
const app = express();
app.use(express.json());

let items = [
  { id: 1, name: 'Item 1' },
  { id: 2, name: 'Item 2' }
];

// GET all items
app.get('/api/items', (req, res) => {
  res.json(items);
});

// POST a new item
app.post('/api/items', (req, res) => {
  const newItem = { id: items.length + 1, name: req.body.name };
  items.push(newItem);
  res.status(201).json(newItem);
});

app.listen(3000, () => console.log('Server running on port 3000'));
```
*(The model followed with 3 paragraphs defining what HTTP verbs mean and asked 10 clarifying questions: "1. What programming language do you prefer? 2. What database are you using? 3. Do you need authentication? 4. What is your business logic? ...")*

### Four Analysis Notes (Baseline Evaluation)
1. **What changed in the prompt:** Baseline prompt — zero layers applied.
2. **What actually improved in the output:** Nothing; this is the baseline. It produced a generic, textbook Node.js in-memory list.
3. **What still failed:** The output is completely useless for real engineering: it guessed a random language (JavaScript/Node), guessed an irrelevant domain (toy items array), stored state in a volatile in-memory variable, included textbook explanations of HTTP, and ended with a wall of 10 clarifying questions.
4. **What I would try next:** Add **a clearer goal** specifying the exact business and technical objective (user authentication, password resets, and session token generation).

---

## 🪜 Step 1: Layer 1 — Clearer Goal (Run 1)

### Added Layer
**A clearer goal**

### The Prompt
```text
Write backend code to implement user authentication, password reset with secure tokens, and session token generation for a SaaS application.
```

### Representative Output Excerpt
```python
from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'

def get_db():
    conn = sqlite3.connect('users.db')
    return conn

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (email, password) VALUES (?, ?)", (data['email'], hashed_password))
    conn.commit()
    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", (data['email'],))
    user = cursor.fetchone()
    if user and check_password_hash(user[2], data['password']):
        token = jwt.encode({'user_id': user[0], 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)}, app.config['SECRET_KEY'])
        return jsonify({'token': token})
    return jsonify({'message': 'Invalid credentials'}), 401
```

### Four Analysis Notes
1. **What changed in the prompt:** Replaced the open-ended query with a concrete technical objective: user authentication, password resets, and session token generation for a SaaS app.
2. **What actually improved in the output:** The model completely stopped generating generic "item/todo" CRUD examples and stopped outputting elementary definitions of HTTP methods. The output focused 100% on the auth domain: password hashing with Werkzeug, user registration, credential verification, and JWT generation.
3. **What still failed:** The model guessed a synchronous Python Flask stack backed by raw SQLite queries (`users.db`). In a high-throughput SaaS backend, synchronous blocking database queries and raw string SQL queries are unacceptable; our stack requires asynchronous FastAPI with PostgreSQL and Redis.
4. **What I would try next:** Add **real context** detailing our production stack (Python 3.11, FastAPI, async SQLAlchemy with asyncpg, and Redis).

---

## 🪜 Step 2: Layer 2 — Real Context (Run 2)

### Added Layer
**Real context**

### The Prompt
```text
Write backend code to implement user authentication, password reset with secure tokens, and session token generation for a SaaS application.

Context: The service is built with Python 3.11 and FastAPI, utilizing PostgreSQL via async SQLAlchemy 2.0 (asyncpg) for persistence and Redis 7.0 for session revocation caching and rate limiting.
```

### Representative Output Excerpt
```python
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, select
import redis.asyncio as aioredis
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
import os

DATABASE_URL = "postgresql+asyncpg://user:pass@localhost:5432/saas_db"
REDIS_URL = "redis://localhost:6379/0"

engine = create_async_engine(DATABASE_URL)
async_session = async_sessionmaker(engine, expire_on_commit=False)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
redis_client = aioredis.from_url(REDIS_URL, decode_responses=True)

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(default=True)

app = FastAPI()

# [... 280 lines of database session dependencies, token validation functions,
# route handlers for /register, /login, /refresh, /reset-password, and Redis blacklist checks,
# all dumped sequentially in a single file ...]
```

### Four Analysis Notes
1. **What changed in the prompt:** Injected specific production context: Python 3.11, FastAPI framework, PostgreSQL with async SQLAlchemy 2.0 (`asyncpg`), and Redis 7.0 for token revocation and rate limiting.
2. **What actually improved in the output:** The output immediately transitioned from synchronous Flask and SQLite to idiomatic asynchronous Python. It adopted `async def` route handlers, `AsyncSession` dependency injection, modern SQLAlchemy 2.0 `Mapped` type annotations, and asynchronous Redis client operations.
3. **What still failed:** The output became a sprawling, 350-line monolithic file. Database configuration, ORM models, cryptographic hashing helpers, Pydantic schemas, and API route handlers were all mashed into a single continuous code block, violating basic separation of concerns.
4. **What I would try next:** Impose **constraints** to restrict code bloat, avoid third-party library dependencies, and keep the solution concise.

---

## 🪜 Step 3: Layer 3 — Constraints (Run 3) — *Honest Regression / "This Made It Worse" Moment*

### Added Layer
**Constraints**

### The Prompt
```text
Write backend code to implement user authentication, password reset with secure tokens, and session token generation for a SaaS application.

Context: The service is built with Python 3.11 and FastAPI, utilizing PostgreSQL via async SQLAlchemy 2.0 (asyncpg) for persistence and Redis 7.0 for session revocation caching and rate limiting.

Constraints: Do not use any third-party auth packages or cryptographic libraries (like passlib, bcrypt, or python-jose); rely only on Python standard libraries; keep the total response under 60 lines of code; do not include comments or docstrings.
```

### Representative Output Excerpt
```python
import hashlib, hmac, json, base64, time
from fastapi import FastAPI, HTTPException, Request

app = FastAPI()
SECRET = "insecure-hardcoded-secret"

def hash_pw(pw: str) -> str:
    return hashlib.sha256(pw.encode()).hexdigest()

def make_token(uid: str) -> str:
    payload = base64.b64encode(json.dumps({"uid": uid, "exp": time.time() + 3600}).encode()).decode()
    sig = hmac.new(SECRET.encode(), payload.encode(), hashlib.sha256).hexdigest()
    return f"{payload}.{sig}"

def check_token(tok: str):
    p, s = tok.split(".")
    if hmac.new(SECRET.encode(), p.encode(), hashlib.sha256).hexdigest() != s: raise HTTPException(401)
    data = json.loads(base64.b64decode(p.encode()).decode())
    if data["exp"] < time.time(): raise HTTPException(401)
    return data["uid"]

@app.post("/login")
async def login(req: Request):
    b = await req.json()
    if b.get("pw") == "admin": return {"tok": make_token(b["user"])}
    raise HTTPException(401)
```

### Four Analysis Notes (Honest Regression Analysis)
1. **What changed in the prompt:** Imposed strict negative constraints: banned external crypto/auth libraries (passlib, bcrypt, python-jose), enforced standard library only, capped line count at <60 lines, and banned docstrings and comments.
2. **What actually improved in the output:** Output length collapsed from 350 lines down to 32 lines. The response avoided verbose preamble and rambling boilerplate.
3. **What still failed (Honest "This made it worse" moment):** **This change created a severe security and functional disaster.**
   - In attempting to satisfy standard-library-only crypto and the <60 line limit, the model abandoned password hashing best practices, using unsalted `hashlib.sha256` which is trivially vulnerable to rainbow tables.
   - It concocted a dangerous, fragile homebrew JWT implementation without timing-attack resistance (`!= s` instead of `hmac.compare_digest`).
   - It threw away database persistence and Redis session checks entirely, hardcoding fake credentials (`"admin"`).
   - In trying to prevent code bloat through negative constraints, we forced the AI to strip out essential architectural and security protections.
4. **What I would try next:** Abandon negative compression constraints. Instead, add **a specified output format** that dictates clean, modular separation of concerns across production-grade architectural layers.

---

## 🪜 Step 4: Layer 4 — Specified Output Format (Run 4)

### Added Layer
**A specified output format**

### The Prompt
```text
Write backend code to implement user authentication, password reset with secure tokens, and session token generation for a SaaS application.

Context: The service is built with Python 3.11 and FastAPI, utilizing PostgreSQL via async SQLAlchemy 2.0 (asyncpg) for persistence and Redis 7.0 for session revocation caching and rate limiting.

Specified output format: Present the solution as three distinct, production-ready modules formatted in separate markdown code blocks with explicit file headers:
1. `app/schemas/auth.py`: Pydantic v2 schemas for UserRegisterRequest, UserLoginRequest, TokenResponse, and PasswordResetRequest.
2. `app/core/security.py`: Password hashing utilities using passlib[bcrypt] and JWT issuance/validation using python-jose.
3. `app/api/v1/auth.py`: FastAPI APIRouter endpoints for /register, /login, /reset-password, and /logout with proper dependency injection.
```

### Representative Output Excerpt
```python
# ==========================================
# File: app/schemas/auth.py
# ==========================================
from pydantic import BaseModel, EmailStr, Field

class UserRegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)

class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int

class PasswordResetRequest(BaseModel):
    email: EmailStr
```
```python
# ==========================================
# File: app/core/security.py
# ==========================================
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "CHANGE_IN_PRODUCTION"
ALGORITHM = "HS256"

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire, "jti": data.get("jti")})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
```
```python
# ==========================================
# File: app/api/v1/auth.py
# ==========================================
from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.auth import UserRegisterRequest, UserLoginRequest, TokenResponse
from app.core.security import verify_password, get_password_hash, create_access_token
# [... Clean FastAPI routes utilizing Depends(get_db) and Depends(get_redis) ...]
```

### Four Analysis Notes
1. **What changed in the prompt:** Specified an exact 3-file module structure (`schemas/auth.py`, `core/security.py`, and `api/v1/auth.py`) with explicit file responsibilities and library assignments.
2. **What actually improved in the output:** The code broke out of the single-file swamp and adopted clean architectural separation of concerns. Pydantic request models, cryptographic utilities, and FastAPI routers were isolated into clean modules matching enterprise backend standards.
3. **What still failed:** The code looks complete on the surface, but there is zero automated verification. There is no proof that Redis token invalidation works during logout, no guarantee that expired tokens return the expected 401 error format, and no test fixtures to simulate failure modes.
4. **What I would try next:** Add **verification requirements** that demand an automated test suite verifying both happy and edge cases.

---

## 🪜 Step 5: Layer 5 — Verification Requirements (Run 5)

### Added Layer
**Verification requirements**

### The Prompt
```text
Write backend code to implement user authentication, password reset with secure tokens, and session token generation for a SaaS application.

Context: The service is built with Python 3.11 and FastAPI, utilizing PostgreSQL via async SQLAlchemy 2.0 (asyncpg) for persistence and Redis 7.0 for session revocation caching and rate limiting.

Specified output format: Present the solution as three distinct, production-ready modules formatted in separate markdown code blocks with explicit file headers:
1. `app/schemas/auth.py`: Pydantic v2 schemas for UserRegisterRequest, UserLoginRequest, TokenResponse, and PasswordResetRequest.
2. `app/core/security.py`: Password hashing utilities using passlib[bcrypt] and JWT issuance/validation using python-jose.
3. `app/api/v1/auth.py`: FastAPI APIRouter endpoints for /register, /login, /reset-password, and /logout with proper dependency injection.

Verification requirements: Provide a fourth module `tests/test_auth.py` containing an asynchronous pytest suite (using pytest-asyncio and httpx.AsyncClient) that rigorously asserts:
1. Successful user registration and subsequent login returns a valid JWT with expected claims.
2. Attempted login with an invalid password returns HTTP 401 Unauthorized with detail 'Invalid credentials'.
3. Decoding an expired JWT raises an HTTP 401 token expired error.
4. Logging out adds the token JTI to Redis and subsequent calls with that token are rejected as revoked.
```

### Representative Output Excerpt
```python
# ==========================================
# File: tests/test_auth.py
# ==========================================
import pytest
from httpx import AsyncClient, ASGITransport
from datetime import timedelta
from app.main import app
from app.core.security import create_access_token

@pytest.mark.asyncio
async def test_register_and_login_success(mock_db_session, mock_redis):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        reg_resp = await client.post("/api/v1/auth/register", json={
            "email": "engineer@saas.com",
            "password": "SecurePassword123!"
        })
        assert reg_resp.status_code == 201

        login_resp = await client.post("/api/v1/auth/login", json={
            "email": "engineer@saas.com",
            "password": "SecurePassword123!"
        })
        assert login_resp.status_code == 200
        data = login_resp.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

@pytest.mark.asyncio
async def test_login_invalid_password(mock_db_session):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.post("/api/v1/auth/login", json={
            "email": "engineer@saas.com",
            "password": "WrongPassword!"
        })
        assert resp.status_code == 401
        assert resp.json()["detail"] == "Invalid credentials"

@pytest.mark.asyncio
async def test_expired_token_rejected(mock_redis):
    expired_token = create_access_token(
        data={"sub": "engineer@saas.com", "jti": "test-jti-expired"},
        expires_delta=timedelta(seconds=-10)
    )
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/api/v1/protected", headers={"Authorization": f"Bearer {expired_token}"})
        assert resp.status_code == 401
        assert "Token expired" in resp.json()["detail"]

@pytest.mark.asyncio
async def test_revoked_token_in_redis_blocked(mock_redis):
    token = create_access_token(
        data={"sub": "engineer@saas.com", "jti": "revoked-jti-123"},
        expires_delta=timedelta(minutes=15)
    )
    # Simulate logout storing JTI in Redis blocklist
    await mock_redis.set("bl:revoked-jti-123", "true", ex=900)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/api/v1/protected", headers={"Authorization": f"Bearer {token}"})
        assert resp.status_code == 401
        assert resp.json()["detail"] == "Token has been revoked"
```

### Four Analysis Notes
1. **What changed in the prompt:** Added formal verification requirements defining an asynchronous test suite (`tests/test_auth.py`) with 4 explicit assertions: valid flow, invalid credentials 401, expired token handling, and Redis JTI revocation.
2. **What actually improved in the output:** The model provided an automated test suite. Crucially, in order to write tests with mockable sessions and Redis instances, **the model refactored the router code in `app/api/v1/auth.py`** to use clean FastAPI dependency injection (`get_db`, `get_redis`). The verification layer acted as an architectural forcing function.
3. **What still failed:** The prompt was tailored to this single auth problem. If another developer on our team wanted to use this prompt for a Billing or Notification module, they would have to reverse-engineer which parts were structural and which were task-specific.
4. **What I would try next:** Clean up and parameterize the prompt into a reusable template that any engineer on the backend track can pick up and run with zero onboarding.

---

## 🎯 Final Reusable Prompt (Cleaned Up for Any Engineer)

Here is the final prompt, abstracted and structured into a reusable engineering template. Any software engineer on the backend track can copy this prompt, fill out the parameterized brackets, and receive production-grade, modular, verified code:

```markdown
Role: Senior Backend Infrastructure Engineer
Objective: Implement [FEATURE_NAME] for our [DOMAIN_TYPE] backend service.

Context & Environment:
- Language & Runtime: Python 3.11+
- Framework: FastAPI (modern async patterns, dependency injection)
- Persistence: PostgreSQL via SQLAlchemy 2.0 (asyncpg, DeclarativeBase, Mapped types)
- Cache & Session Store: Redis 7.0 (redis.asyncio)
- Secret Management: Configuration via pydantic-settings BaseSettings reading environment variables

Requirements & Business Logic:
[DETAILED_FEATURE_SPECS_AND_RULES]

Specified Output Format:
Organize the implementation across clean, modular files with explicit markdown file headers:
1. `app/schemas/[MODULE].py`: Strict Pydantic v2 schemas for all Request, Response, and Event models.
2. `app/core/[UTILITY].py`: Reusable domain logic, security routines, or external client helpers.
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

## 🔬 Key Takeaway: The Value of Discipline

| Layer Added | Primary Benefit Realized | What We Learned |
|---|---|---|
| **Goal** | Eliminated generic guesswork and 10 clarifying questions | Without a clear goal, LLMs generate introductory textbook explanations. |
| **Context** | Upgraded tech stack from toy Flask/SQLite to async FastAPI/Postgres | AI reflects your architecture only when you define the runtime reality. |
| **Constraints** *(Regression)* | Forced brevity but broke security and architecture | **Arbitrary negative constraints ("keep under 60 lines") destroy code safety.** |
| **Output Format** | Organized code into clean, production-grade modular files | Format instructions work far better than negative constraints for enforcing structure. |
| **Verification** | Forced dependency injection and validated edge cases | Requiring tests forces the model to generate testable, decoupled application code. |
