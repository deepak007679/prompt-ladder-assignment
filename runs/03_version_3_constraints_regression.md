# Run 3: Layer 3 — Constraints (Honest Regression / "This Made It Worse")

## 🏷️ Layer Added
**Constraints**

---

## 📌 Prompt
```text
Write backend code to implement user authentication, password reset with secure tokens, and session token generation for a SaaS application.

Context: The service is built with Python 3.11 and FastAPI, utilizing PostgreSQL via async SQLAlchemy 2.0 (asyncpg) for persistence and Redis 7.0 for session revocation caching and rate limiting.

Constraints: Do not use any third-party auth packages or cryptographic libraries (like passlib, bcrypt, or python-jose); rely only on Python standard libraries; keep the total response under 60 lines of code; do not include comments or docstrings.
```

---

## 💻 Full Representative Output
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

def verify_token(tok: str) -> str:
    try:
        p, s = tok.split(".")
        if hmac.new(SECRET.encode(), p.encode(), hashlib.sha256).hexdigest() != s:
            raise HTTPException(401, "Invalid signature")
        data = json.loads(base64.b64decode(p.encode()).decode())
        if data["exp"] < time.time():
            raise HTTPException(401, "Expired")
        return data["uid"]
    except Exception:
        raise HTTPException(401, "Invalid token")

@app.post("/register")
async def register(req: Request):
    b = await req.json()
    return {"status": "ok", "hash": hash_pw(b["password"])}

@app.post("/login")
async def login(req: Request):
    b = await req.json()
    if b.get("username") == "admin" and b.get("password") == "pass":
        return {"token": make_token("1")}
    raise HTTPException(401, "Unauthorized")

@app.post("/reset-request")
async def reset_req(req: Request):
    b = await req.json()
    return {"reset_token": make_token(b.get("email"))}
```

---

## 🔍 Four Mandatory Analysis Notes

1. **What changed in the prompt:**  
   Added negative constraints: banned external auth and crypto packages (passlib, bcrypt, python-jose), restricted code to Python standard library only, imposed a strict ceiling of <60 lines of code, and prohibited comments/docstrings.
2. **What actually improved in the output:**  
   Response volume plummeted from ~350 lines down to 40 lines. The model stopped generating expansive boilerplate and delivered a tight snippet within the requested size envelope.
3. **What still failed (Honest "This made it worse" moment):**  
   **This iteration represents a catastrophic regression in code quality and security:**
   - **Critical Vulnerability (Unsalted Hashing):** To avoid third-party libraries under standard library constraints, the model resorted to unsalted `hashlib.sha256()`. This makes password hashes trivially crackable via rainbow tables and violates OWASP compliance.
   - **Timing Attack Vulnerability:** The signature check used direct string comparison (`!= s`) rather than constant-time comparison (`hmac.compare_digest`), opening the door to side-channel timing attacks.
   - **Complete Loss of Architecture:** To satisfy the 60-line cap, the model completely deleted PostgreSQL integration, SQLAlchemy models, and Redis session tracking. It replaced real database storage with hardcoded dummy checks (`if username == "admin"`).
   - **Loss of Type Safety:** It eliminated Pydantic schemas, parsing untyped JSON directly from `await req.json()`.
   - **Takeaway:** Imposing blunt negative constraints ("standard libraries only", "<60 lines") forced the model to sacrifice production security and architecture to satisfy arbitrary brevity rules.
4. **What I would try next:**  
   Remove the destructive brevity and standard-lib constraints. Instead, add **a specified output format** that structures the output into separate, production-ready modules across explicit file boundaries while utilizing secure, industry-standard libraries.
