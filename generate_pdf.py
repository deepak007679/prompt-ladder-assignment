import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether, PageBreak, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_header_footer(num_pages)
            super().showPage()
        super().save()

    def draw_header_footer(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        
        # Header (on pages after cover/first page)
        if self._pageNumber > 1:
            self.drawString(54, 755, "Prompt Engineering Assignment: The Prompt Ladder | Implementation Report")
            self.drawRightString(558, 755, "Track: Backend Engineering")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.75)
            self.line(54, 747, 558, 747)

        # Footer (all pages)
        footer_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 36, footer_text)
        self.drawString(54, 36, "Author: Deepak | github.com/deepak007679/prompt-ladder-assignment")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.75)
        self.line(54, 48, 558, 48)
        self.restoreState()

def create_report():
    output_pdf = r"C:\Users\Deepak\.gemini\antigravity\scratch\prompt-ladder-assignment\Prompt_Ladder_Implementation_Report.pdf"
    doc = SimpleDocTemplate(
        output_pdf,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=colors.HexColor("#0F172A"),
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#475569"),
        spaceAfter=14
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=19,
        textColor=colors.HexColor("#1E293B"),
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor("#2563EB"),
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor("#334155"),
        spaceAfter=6
    )

    body_bold = ParagraphStyle(
        'Body_Bold',
        parent=body_style,
        fontName='Helvetica-Bold'
    )

    code_block_style = ParagraphStyle(
        'CodeBlock',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor("#0F172A"),
        backColor=colors.HexColor("#F1F5F9"),
        borderColor=colors.HexColor("#CBD5E1"),
        borderWidth=0.5,
        borderPadding=6,
        spaceBefore=4,
        spaceAfter=6
    )

    prompt_box_style = ParagraphStyle(
        'PromptBox',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=9,
        leading=12.5,
        textColor=colors.HexColor("#1E3A8A"),
        backColor=colors.HexColor("#EFF6FF"),
        borderColor=colors.HexColor("#93C5FD"),
        borderWidth=0.75,
        borderPadding=6,
        spaceBefore=4,
        spaceAfter=6
    )

    alert_box_style = ParagraphStyle(
        'AlertBox',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#991B1B"),
        backColor=colors.HexColor("#FEF2F2"),
        borderColor=colors.HexColor("#F87171"),
        borderWidth=0.75,
        borderPadding=6,
        spaceBefore=4,
        spaceAfter=6
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.white
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor("#1E293B")
    )

    story = []

    # 1. Document Header
    story.append(Paragraph("Prompt Engineering: The Prompt Ladder", title_style))
    story.append(Paragraph("Systematic Layer-by-Layer Optimization in Backend Engineering | Implementation Report", subtitle_style))

    # Metadata Box
    meta_data = [
        [
            Paragraph("<b>Author:</b> Deepak", table_cell_style),
            Paragraph("<b>Track:</b> Backend & Distributed Systems", table_cell_style),
            Paragraph("<b>Runtime:</b> Python 3.11 / FastAPI / asyncpg / Redis", table_cell_style)
        ],
        [
            Paragraph("<b>GitHub:</b> <font color='#2563EB'><u>github.com/deepak007679/prompt-ladder-assignment</u></font>", table_cell_style),
            Paragraph("<b>Runs Total:</b> 6 (Baseline + 5 Layers)", table_cell_style),
            Paragraph("<b>Date:</b> October 2026", table_cell_style)
        ]
    ]
    t_meta = Table(meta_data, colWidths=[180, 160, 164])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('BOX', (0,0), (-1,-1), 0.75, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 12))

    # 2. Executive Rationale & Methodology
    story.append(Paragraph("1. Executive Rationale & Methodology", h1_style))
    story.append(Paragraph(
        "The gap between a lazy prompt and an engineered one is the cheapest performance upgrade in AI, yet most engineers never witness it because they modify multiple variables simultaneously. "
        "This project adheres to strict experimental discipline: <b>one isolated layer is introduced per version</b>, attacking the primary weakness identified in the preceding output. "
        "Furthermore, by closely inspecting behavioral deltas rather than superficial changes, we captured an authentic <b>regression failure in Run 3</b>, demonstrating how misguided negative constraints degrade production software.",
        body_style
    ))

    # 3. Progression Summary Table
    story.append(Spacer(1, 4))
    story.append(Paragraph("2. The Prompt Ladder Matrix (Overview of 6 Runs)", h1_style))
    
    matrix_data = [
        [
            Paragraph("Run", table_header_style),
            Paragraph("Layer Added", table_header_style),
            Paragraph("Prompt Focus", table_header_style),
            Paragraph("What Actually Improved in Output", table_header_style),
            Paragraph("Remaining Flaw / Regression", table_header_style)
        ],
        [
            Paragraph("<b>Run 0</b>", table_cell_style),
            Paragraph("Baseline", table_cell_style),
            Paragraph('"Write backend code"', table_cell_style),
            Paragraph("None (Baseline starting point)", table_cell_style),
            Paragraph("Guessed Node.js, generic items array, 10 scoping questions.", table_cell_style)
        ],
        [
            Paragraph("<b>Run 1</b>", table_cell_style),
            Paragraph("Clearer Goal", table_cell_style),
            Paragraph("User auth, password reset, session tokens", table_cell_style),
            Paragraph("Stopped asking 10 scoping questions; focused 100% on auth domain.", table_cell_style),
            Paragraph("Guessed synchronous Flask with direct SQLite connections and raw SQL.", table_cell_style)
        ],
        [
            Paragraph("<b>Run 2</b>", table_cell_style),
            Paragraph("Real Context", table_cell_style),
            Paragraph("Python 3.11, FastAPI, async SQLAlchemy 2.0, Redis", table_cell_style),
            Paragraph("Adopted async/await, asyncpg, DeclarativeBase Mapped models, Redis pools.", table_cell_style),
            Paragraph("350-line monolithic single-file code dump mixing all layers.", table_cell_style)
        ],
        [
            Paragraph("<b>Run 3</b>", table_cell_style),
            Paragraph("<font color='#DC2626'><b>Constraints</b><br/>(Regression)</font>", table_cell_style),
            Paragraph("Stdlib only, <60 lines, no comments", table_cell_style),
            Paragraph("Output compressed to 40 lines; zero rambling prose.", table_cell_style),
            Paragraph("<font color='#DC2626'><b>CRITICAL BREAKDOWN:</b> Unsalted SHA-256, timing attacks, stripped DB & Redis.</font>", table_cell_style)
        ],
        [
            Paragraph("<b>Run 4</b>", table_cell_style),
            Paragraph("Specified Output Format", table_cell_style),
            Paragraph("3 modular files: schemas, core/security, api/v1", table_cell_style),
            Paragraph("Clean architectural boundaries; separated validation, crypto, and routing.", table_cell_style),
            Paragraph("Zero automated verification that tokens, expiry, or Redis revocation work.", table_cell_style)
        ],
        [
            Paragraph("<b>Run 5</b>", table_cell_style),
            Paragraph("Verification Requirements", table_cell_style),
            Paragraph("Async pytest suite: happy path, 401, expiry, Redis block", table_cell_style),
            Paragraph("Generated executable pytest tests; forced router to use mockable Depends.", table_cell_style),
            Paragraph("Hardcoded to single microservice scenario; needed parameterization.", table_cell_style)
        ]
    ]

    t_matrix = Table(matrix_data, colWidths=[38, 85, 105, 138, 138])
    t_matrix.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1E293B")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_matrix)
    story.append(Spacer(1, 14))

    # Page Break for Step-by-Step Deep Dive
    story.append(PageBreak())

    # 4. Detailed Run Breakdown
    story.append(Paragraph("3. Detailed Run Analysis & Four-Note Evaluations", h1_style))

    runs = [
        {
            "num": "Run 0: Baseline (The Lazy Prompt)",
            "layer": "None (Unconstrained Baseline)",
            "prompt": "Write backend code",
            "excerpt": "// Node.js / Express\nconst express = require('express');\nconst app = express();\nlet items = [{ id: 1, name: 'Item One' }];\napp.get('/api/items', (req, res) => res.json(items));\napp.post('/api/items', (req, res) => { items.push(req.body); res.status(201).json(req.body); });\napp.listen(3000);\n\n// Followed by definitions of GET/POST and 10 clarifying questions...",
            "notes": [
                ("What changed in the prompt", "Zero layers applied. A genuinely weak and unguided directive."),
                ("What actually improved in the output", "Baseline reference point; no improvements."),
                ("What still failed", "Guessed arbitrary language (Node.js), invented a toy in-memory array, explained basic HTTP verbs, and asked 10 scoping questions."),
                ("What I would try next", "Add a clearer goal targeting user authentication, password reset, and session tokens.")
            ],
            "alert": None
        },
        {
            "num": "Run 1: Layer 1 — Clearer Goal",
            "layer": "A clearer goal",
            "prompt": "Write backend code to implement user authentication, password reset with secure tokens, and session token generation for a SaaS application.",
            "excerpt": "from flask import Flask, request, jsonify\nimport jwt, sqlite3\n\n@app.route('/login', methods=['POST'])\ndef login():\n    # queries sqlite3 auth.db, verifies password, encodes HS256 JWT\n    token = jwt.encode({'user_id': user[0], 'exp': ...}, 'secret')\n    return jsonify({'access_token': token})",
            "notes": [
                ("What changed in the prompt", "Specified the domain goal: user authentication, password reset, and session token issuance for SaaS."),
                ("What actually improved in the output", "The model completely ceased generating toy item CRUD arrays and dropped textbook explanations. Output focused 100% on authentication mechanisms."),
                ("What still failed", "Assumed a synchronous Flask stack with direct unpooled SQLite queries (auth.db) and raw SQL strings, unsuitable for high-concurrency SaaS."),
                ("What I would try next", "Add real context specifying Python 3.11, FastAPI, async SQLAlchemy 2.0 (asyncpg), and Redis 7.0.")
            ],
            "alert": None
        },
        {
            "num": "Run 2: Layer 2 — Real Context",
            "layer": "Real context",
            "prompt": "Write backend code to implement user authentication, password reset with secure tokens, and session token generation for a SaaS application.\n\nContext: The service is built with Python 3.11 and FastAPI, utilizing PostgreSQL via async SQLAlchemy 2.0 (asyncpg) for persistence and Redis 7.0 for session revocation caching and rate limiting.",
            "excerpt": "from fastapi import FastAPI, Depends\nfrom sqlalchemy.ext.asyncio import AsyncSession\nimport redis.asyncio as aioredis\n\n# [... 350 lines combining models, schemas, password hashing, \n# routes, and Redis revocation into a single monolithic file ...]",
            "notes": [
                ("What changed in the prompt", "Injected production environment: Python 3.11, FastAPI, asyncpg, DeclarativeBase ORM, and Redis 7.0."),
                ("What actually improved in the output", "Eliminated synchronous blocking code. Instantly adopted async def endpoints, AsyncSession dependencies, SQLAlchemy Mapped types, and Redis async revocation."),
                ("What still failed", "Produced a 350-line monolithic blob where database models, Pydantic schemas, crypto helpers, and endpoints were smashed together without modular separation."),
                ("What I would try next", "Add constraints to force brevity and avoid heavy third-party dependencies.")
            ],
            "alert": None
        },
        {
            "num": "Run 3: Layer 3 — Constraints (Honest Regression / 'This Made It Worse')",
            "layer": "Constraints",
            "prompt": "Write backend code to implement user authentication, password reset with secure tokens, and session token generation for a SaaS application.\n\nContext: The service is built with Python 3.11 and FastAPI, utilizing PostgreSQL via async SQLAlchemy 2.0 (asyncpg) for persistence and Redis 7.0 for session revocation caching and rate limiting.\n\nConstraints: Do not use any third-party auth packages or cryptographic libraries (like passlib, bcrypt, or python-jose); rely only on Python standard libraries; keep the total response under 60 lines of code; do not include comments or docstrings.",
            "excerpt": "def hash_pw(pw: str) -> str:\n    return hashlib.sha256(pw.encode()).hexdigest() # CRITICAL VULNERABILITY: UNSALTED!\n\ndef make_token(uid: str) -> str:\n    # Insecure base64 + hmac token without constant-time comparison\n    sig = hmac.new(SECRET.encode(), payload.encode(), hashlib.sha256).hexdigest()\n    return f\"{payload}.{sig}\"\n\n@app.post(\"/login\")\nasync def login(req: Request):\n    if b.get(\"pw\") == \"admin\": return {\"tok\": make_token(b[\"user\"])} # HARDCODED!",
            "notes": [
                ("What changed in the prompt", "Imposed blunt negative constraints: standard libraries only, under 60 lines, and no comments."),
                ("What actually improved in the output", "Output compressed to 40 lines; eliminated rambling explanations."),
                ("What still failed (Honest 'Made it worse')", "SEVERE QUALITY & SECURITY BREAKDOWN: Unsalted SHA-256 (vulnerable to rainbow tables), homebrew tokens vulnerable to timing attacks (used != instead of compare_digest), deleted all PostgreSQL and Redis code, and hardcoded 'admin' credentials. Negative brevity constraints broke production viability."),
                ("What I would try next", "Abandon negative compression constraints. Replace them with a specified output format enforcing clean modular files.")
            ],
            "alert": "HONEST REGRESSION IDENTIFIED: Imposing arbitrary negative constraints (<60 lines, standard libraries only) caused a critical failure mode where the model traded security compliance and architectural integrity for superficial brevity."
        },
        {
            "num": "Run 4: Layer 4 — Specified Output Format",
            "layer": "A specified output format",
            "prompt": "Write backend code to implement user authentication, password reset with secure tokens, and session token generation for a SaaS application.\n\nContext: The service is built with Python 3.11 and FastAPI, utilizing PostgreSQL via async SQLAlchemy 2.0 (asyncpg) for persistence and Redis 7.0 for session revocation caching and rate limiting.\n\nSpecified output format: Present the solution as three distinct, production-ready modules formatted in separate markdown code blocks with explicit file headers:\n1. `app/schemas/auth.py`: Pydantic v2 schemas\n2. `app/core/security.py`: Password hashing (passlib[bcrypt]) and JWT (python-jose)\n3. `app/api/v1/auth.py`: FastAPI APIRouter endpoints with dependency injection.",
            "excerpt": "### app/schemas/auth.py\nclass UserRegisterRequest(BaseModel): ...\n\n### app/core/security.py\npwd_context = CryptContext(schemes=[\"bcrypt\"], deprecated=\"auto\")\ndef create_access_token(...) -> tuple[str, str]: ...\n\n### app/api/v1/auth.py\n@router.post(\"/login\", response_model=TokenResponse)\nasync def login(payload: UserLoginRequest, db: AsyncSession = Depends(get_db)): ...",
            "notes": [
                ("What changed in the prompt", "Replaced negative brevity rules with a 3-tier modular file layout (schemas, security core, and API routes)."),
                ("What actually improved in the output", "Healed the Run 3 regression while resolving Run 2's monolithic clutter. Created clean, pasteable files with proper separation of concerns matching enterprise standards."),
                ("What still failed", "Zero automated verification. There is no proof that token expiration or Redis blocklisting works as expected under real test vectors."),
                ("What I would try next", "Add verification requirements mandating an async pytest suite testing success, 401 errors, expired tokens, and Redis revocation.")
            ],
            "alert": None
        },
        {
            "num": "Run 5: Layer 5 — Verification Requirements",
            "layer": "Verification requirements",
            "prompt": "[Prior prompt from Run 4] + \nVerification requirements: Provide a fourth module `tests/test_auth.py` containing an asynchronous pytest suite (using pytest-asyncio and httpx.AsyncClient) asserting: 1) register & login JWT issuance, 2) invalid password returns HTTP 401, 3) expired JWT returns 401, 4) logout revokes token in Redis.",
            "excerpt": "# tests/test_auth.py\n@pytest.mark.asyncio\nasync def test_auth_full_lifecycle_success(mock_redis):\n    app.dependency_overrides[get_redis] = lambda: mock_redis\n    async with AsyncClient(transport=ASGITransport(app=app), base_url=\"http://test\") as client:\n        # Tests register, login, protected endpoint, logout, and token revocation block",
            "notes": [
                ("What changed in the prompt", "Added verification requirements specifying an automated async pytest suite testing 4 explicit test vectors."),
                ("What actually improved in the output", "Acted as an architectural forcing function. To make the test suite work with mocks, the model refactored the router to expose clean Depends(get_db) and Depends(get_redis) injection, dramatically increasing testability."),
                ("What still failed", "The prompt was hardcoded to this single auth microservice; it was not yet parameterized for other backend modules."),
                ("What I would try next", "Generalize into a clean, reusable template with parameter brackets for any backend engineer.")
            ],
            "alert": None
        }
    ]

    for r in runs:
        story.append(Paragraph(r['num'], h2_style))
        story.append(Paragraph(f"<b>Added Layer:</b> <font color='#2563EB'>{r['layer']}</font>", body_style))
        story.append(Paragraph("<b>Prompt:</b>", body_style))
        story.append(Paragraph(r['prompt'].replace('\n', '<br/>'), prompt_box_style))
        story.append(Paragraph("<b>Representative Output Excerpt:</b>", body_style))
        story.append(Paragraph(r['excerpt'].replace('\n', '<br/>'), code_block_style))

        if r['alert']:
            story.append(Paragraph(r['alert'], alert_box_style))

        notes_table_data = [
            [Paragraph(f"<b>{title}:</b>", body_bold), Paragraph(content, body_style)]
            for title, content in r['notes']
        ]
        t_notes = Table(notes_table_data, colWidths=[160, 344])
        t_notes.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
            ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#F1F5F9")),
            ('TOPPADDING', (0,0), (-1,-1), 3),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3),
            ('LEFTPADDING', (0,0), (-1,-1), 6),
            ('RIGHTPADDING', (0,0), (-1,-1), 6),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ]))
        story.append(t_notes)
        story.append(Spacer(1, 10))

    # Page Break for Final Reusable Template
    story.append(PageBreak())

    # 5. Final Reusable Prompt
    story.append(Paragraph("4. Final Reusable Prompt Template (Stranger-Ready)", h1_style))
    story.append(Paragraph(
        "Through empirical iterations, the prompt was transformed from an embarrassing 3-word query into a battle-tested engineering template. "
        "It is packaged with parameterized variable slots so any backend engineer on the team can achieve production-grade code on the first generation without author supervision:",
        body_style
    ))

    template_code = (
        "Role: Senior Backend Infrastructure Engineer\n"
        "Objective: Implement [FEATURE_NAME] for our [DOMAIN_TYPE] backend service.\n\n"
        "Context & Environment:\n"
        "- Language & Runtime: Python 3.11+\n"
        "- Framework: FastAPI (modern asynchronous patterns, dependency injection)\n"
        "- Persistence: PostgreSQL via SQLAlchemy 2.0 (asyncpg, DeclarativeBase, Mapped types)\n"
        "- Cache & Session Store: Redis 7.0 (redis.asyncio)\n"
        "- Secret Management: Configuration via pydantic-settings BaseSettings reading env vars\n\n"
        "Requirements & Business Logic:\n"
        "1. [REQUIREMENT_1 - e.g., Email validation and salted bcrypt password hashing]\n"
        "2. [REQUIREMENT_2 - e.g., JWT access token issuance (15m exp) and rotation]\n"
        "3. [REQUIREMENT_3 - e.g., Token revocation endpoint on logout that blacklists JTI in Redis]\n\n"
        "Specified Output Format:\n"
        "Organize the implementation across clean, modular files with explicit markdown file headers:\n"
        "1. `app/schemas/[MODULE].py`: Strict Pydantic v2 schemas for Request/Response models.\n"
        "2. `app/core/[UTILITY].py`: Reusable domain logic, security routines, and hashing helpers.\n"
        "3. `app/api/v1/[MODULE].py`: FastAPI APIRouter endpoints using Depends for DB and cache.\n"
        "4. `tests/test_[MODULE].py`: Asynchronous test suite using pytest-asyncio and httpx.AsyncClient.\n\n"
        "Verification & Quality Criteria:\n"
        "- Do not omit implementation details with '# TODO: implement later' placeholders.\n"
        "- Ensure all route exceptions raise typed HTTPException with RFC-7807 compliant error details.\n"
        "- All database operations must commit or rollback cleanly within async session contexts.\n"
        "- The test suite in tests/test_[MODULE].py must assert happy paths, 401 errors, and revocation."
    )
    story.append(Paragraph(template_code.replace('\n', '<br/>'), code_block_style))

    # 6. Conclusion & Verification Artifacts
    story.append(Spacer(1, 10))
    story.append(Paragraph("5. Project Artifacts & GitHub Verification", h1_style))
    story.append(Paragraph(
        "All 6 progression runs, comparative analyses, and the final stranger-ready template have been committed and pushed to GitHub:",
        body_style
    ))

    git_info = [
        [Paragraph("<b>GitHub Repository:</b>", body_bold), Paragraph("<font color='#2563EB'><u>https://github.com/deepak007679/prompt-ladder-assignment</u></font>", table_cell_style)],
        [Paragraph("<b>Local Directory:</b>", body_bold), Paragraph("<code>C:\\Users\\Deepak\\.gemini\\antigravity\\scratch\\prompt-ladder-assignment</code>", table_cell_style)],
        [Paragraph("<b>Primary Deliverable:</b>", body_bold), Paragraph("<code>PROMPT_LADDER.md</code> (Complete 6-run ladder documentation)", table_cell_style)],
        [Paragraph("<b>Reusable Template:</b>", body_bold), Paragraph("<code>final_reusable_prompt.md</code> (Production prompt template)", table_cell_style)],
        [Paragraph("<b>Individual Run Logs:</b>", body_bold), Paragraph("<code>runs/00_baseline.md</code> through <code>runs/05_version_5_verification.md</code>", table_cell_style)],
        [Paragraph("<b>Git Commit:</b>", body_bold), Paragraph("<code>9b978b0</code> (feat: complete prompt ladder assignment with 6 runs and reusable prompt)", table_cell_style)]
    ]
    t_git = Table(git_info, colWidths=[140, 364])
    t_git.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_git)

    # Build PDF
    doc.build(story, canvasmaker=NumberedCanvas)
    print("PDF Generated successfully at:", output_pdf)

if __name__ == '__main__':
    create_report()
