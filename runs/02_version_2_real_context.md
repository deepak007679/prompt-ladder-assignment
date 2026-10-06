# Run 2: Layer 2 — Real Context

## 🏷️ Layer Added
**Real context**

---

## 📌 Prompt
```text
Write backend code to implement user authentication, password reset with secure tokens, and session token generation for a SaaS application.

Context: The service is built with Python 3.11 and FastAPI, utilizing PostgreSQL via async SQLAlchemy 2.0 (asyncpg) for persistence and Redis 7.0 for session revocation caching and rate limiting.
```

---

## 💻 Full Representative Output
```python
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, select, update
import redis.asyncio as aioredis
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from pydantic import BaseModel, EmailStr
import secrets
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:pass@localhost:5432/saas_db")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
SECRET_KEY = os.getenv("JWT_SECRET", "super-secret-key-32-bytes-long")
ALGORITHM = "HS256"

engine = create_async_engine(DATABASE_URL, echo=False)
async_session = async_sessionmaker(engine, expire_on_commit=False)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
redis_pool = aioredis.ConnectionPool.from_url(REDIS_URL)

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    reset_token: Mapped[str | None] = mapped_column(String(255), nullable=True)
    reset_token_exp: Mapped[datetime | None] = mapped_column(nullable=True)

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

app = FastAPI(title="SaaS Auth API")

async def get_db():
    async with async_session() as session:
        yield session

async def get_redis():
    client = aioredis.Redis(connection_pool=redis_pool)
    try:
        yield client
    finally:
        await client.close()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")

@app.post("/api/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(req: RegisterRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == req.email))
    if result.scalars().first():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed = pwd_context.hash(req.password)
    new_user = User(email=req.email, hashed_password=hashed)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    
    token = jwt.encode({"sub": str(new_user.id), "exp": datetime.now(timezone.utc) + timedelta(hours=1)}, SECRET_KEY, algorithm=ALGORITHM)
    return TokenResponse(access_token=token)

@app.post("/api/login", response_model=TokenResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(User).where(User.email == form_data.username))
    user = res.scalars().first()
    if not user or not pwd_context.verify(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = jwt.encode({"sub": str(user.id), "exp": datetime.now(timezone.utc) + timedelta(hours=1)}, SECRET_KEY, algorithm=ALGORITHM)
    return TokenResponse(access_token=token)

@app.post("/api/logout")
async def logout(token: str = Depends(oauth2_scheme), redis: aioredis.Redis = Depends(get_redis)):
    await redis.set(f"bl:{token}", "revoked", ex=3600)
    return {"message": "Logged out successfully"}
```

---

## 🔍 Four Mandatory Analysis Notes

1. **What changed in the prompt:**  
   Injected explicit operational context: Python 3.11, FastAPI framework, async SQLAlchemy 2.0 with asyncpg driver, and Redis 7.0 for session revocation and rate limiting.
2. **What actually improved in the output:**  
   The output instantly aligned with our modern architecture. It eliminated synchronous blocking I/O, embraced `async def` and `async with` idioms, utilized SQLAlchemy 2.0 `Mapped` declarative syntax, used `OAuth2PasswordBearer`, and implemented Redis asynchronous token blacklisting on logout.
3. **What still failed:**  
   The model created a single monolithic 350-line code blob. Database models, Pydantic DTOs, crypto utilities, Redis connection lifecycle, and endpoint routers are all jammed together in one file, which violates our project's modular service layout and maintainability guidelines.
4. **What I would try next:**  
   Add **constraints** to prevent lengthy monolithic output, enforce standard library reliance, and constrain output size.
