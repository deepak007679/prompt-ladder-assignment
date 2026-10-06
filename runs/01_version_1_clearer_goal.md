# Run 1: Layer 1 — Clearer Goal

## 🏷️ Layer Added
**A clearer goal**

---

## 📌 Prompt
```text
Write backend code to implement user authentication, password reset with secure tokens, and session token generation for a SaaS application.
```

---

## 💻 Full Representative Output
```python
from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
import secrets
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key-12345'

def init_db():
    conn = sqlite3.connect('auth.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            reset_token TEXT,
            reset_token_exp TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({'error': 'Email and password required'}), 400
        
    hashed = generate_password_hash(password, method='sha256')
    try:
        conn = sqlite3.connect('auth.db')
        cur = conn.cursor()
        cur.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, hashed))
        conn.commit()
        conn.close()
        return jsonify({'message': 'User registered'}), 201
    except sqlite3.IntegrityError:
        return jsonify({'error': 'User already exists'}), 409

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    conn = sqlite3.connect('auth.db')
    cur = conn.cursor()
    cur.execute("SELECT id, password FROM users WHERE email = ?", (email,))
    user = cur.fetchone()
    conn.close()
    
    if user and check_password_hash(user[1], password):
        token = jwt.encode({
            'user_id': user[0],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=2)
        }, app.config['SECRET_KEY'], algorithm='HS256')
        return jsonify({'access_token': token}), 200
        
    return jsonify({'error': 'Invalid email or password'}), 401

@app.route('/api/request-reset', methods=['POST'])
def request_reset():
    email = request.get_json().get('email')
    token = secrets.token_urlsafe(32)
    exp = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    
    conn = sqlite3.connect('auth.db')
    cur = conn.cursor()
    cur.execute("UPDATE users SET reset_token = ?, reset_token_exp = ? WHERE email = ?", (token, exp, email))
    conn.commit()
    conn.close()
    return jsonify({'reset_token': token, 'message': 'Password reset token generated'}), 200
```

---

## 🔍 Four Mandatory Analysis Notes

1. **What changed in the prompt:**  
   Replaced the vague directive with an explicit technical goal: user authentication, password resets with secure tokens, and session token generation for a SaaS application.
2. **What actually improved in the output:**  
   The output ceased generating toy "item/todo" arrays, stopped defining basic HTTP verbs, and dropped the 10 general scoping questions. It directed 100% of the code toward authentication mechanisms (password hashing, credential validation, JWT creation, and reset token generation).
3. **What still failed:**  
   The model assumed a synchronous Python Flask stack using direct, unpooled SQLite connections (`auth.db`) and raw SQL strings. This is incompatible with high-concurrency SaaS production architectures requiring async I/O, modern ORMs, and separated database connection management.
4. **What I would try next:**  
   Add **real context** defining our production stack: Python 3.11, FastAPI, async SQLAlchemy 2.0 with PostgreSQL (asyncpg), and Redis for session cache and rate limiting.
