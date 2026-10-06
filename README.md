# Prompt Engineering: The Prompt Ladder

> **"The gap between a lazy prompt and an engineered one is the cheapest performance upgrade in AI, and most people never see it because they change five things at once and learn nothing. This assignment forces the discipline: one change at a time, output compared at every step."**

---

## 📌 Executive Summary

This repository documents **The Prompt Ladder**, an empirical, layer-by-layer exploration of prompt optimization for backend engineering. Starting with a genuinely weak and embarrassing baseline prompt (`"Write backend code"`), the prompt is incrementally improved across **five successive versions**.

Each version adds **exactly one named layer** targeting the previous output's primary failure mode:
1. **Run 0 (Baseline)**: Lazy prompt — `"Write backend code"`
2. **Run 1 (+ Clearer Goal)**: Focuses the domain on authentication, reset tokens, and session management.
3. **Run 2 (+ Real Context)**: Anchors the runtime to Python 3.11, FastAPI, async SQLAlchemy (asyncpg), and Redis.
4. **Run 3 (+ Constraints — Honest Regression)**: Imposes standard-library-only and length constraints, causing a **critical security and quality breakdown**.
5. **Run 4 (+ Specified Output Format)**: Replaces negative constraints with an explicit three-tier file architecture.
6. **Run 5 (+ Verification Requirements)**: Demands an automated `pytest-asyncio` suite verifying happy paths, token expiry, 401 errors, and Redis revocation.
7. **Final Deliverable**: A production-grade, stranger-ready prompt template ready for any backend engineer.

---

## 🪜 The Prompt Ladder Matrix

| Run | Added Layer | Core Prompt Delta | Key Output Improvement | Remaining Failure / Regression |
|---|---|---|---|---|
| **0** | Baseline | None (`"Write backend code"`) | None (Unusable toy CRUD & generic questions) | No language, no framework, textbook definitions, 10 clarifying questions |
| **1** | **Clearer Goal** | Defined auth, password reset, and session tokens | Stopped asking 10 scoping questions; focused purely on auth logic | Guessed random synchronous Flask & in-memory SQLite stack |
| **2** | **Real Context** | Added Python 3.11, FastAPI, async SQLAlchemy, Redis | Switched to modern `async/await` syntax, ORM models, and Redis pools | 350-line monolithic file mixing schemas, routes, and crypto |
| **3** | **Constraints** *(Regression)* | Stdlib only, <60 lines, no comments | Output shortened to 48 lines | **CRITICAL REGRESSION**: Used unsalted SHA-256, homebrew base64 tokens, stripped error handling |
| **4** | **Specified Output Format** | Modular 3-file breakdown (`schemas`, `security`, `api`) | Clean architectural boundaries; schemas separated from routes and crypto | Zero automated verification; no proof that token expiry or revocation works |
| **5** | **Verification Requirements** | 4-point async `pytest` test suite | Generated executable test suite with mocked sessions; forced dependency injection | Hardcoded to one service; not reusable across diverse endpoints |
| **Final** | **Reusable Template** | Parameterized fields (`[GOAL]`, `[CONTEXT]`, `[FORMAT]`, etc.) | Fully portable for any engineer on the team without author intervention | Ready for production deployment |

---

## 📁 Repository Structure

```text
prompt-ladder-assignment/
├── README.md                                  # Project overview and matrix (this file)
├── PROMPT_LADDER.md                           # Comprehensive assignment deliverable
├── final_reusable_prompt.md                   # Portable prompt template for backend engineers
└── runs/
    ├── 00_baseline.md                         # Run 0: Weak baseline run and analysis
    ├── 01_version_1_clearer_goal.md           # Run 1: Layer 1 - Clearer Goal
    ├── 02_version_2_real_context.md           # Run 2: Layer 2 - Real Context
    ├── 03_version_3_constraints_regression.md # Run 3: Layer 3 - Constraints (Honest Regression)
    ├── 04_version_4_output_format.md          # Run 4: Layer 4 - Specified Output Format
    └── 05_version_5_verification.md           # Run 5: Layer 5 - Verification Requirements
```

---

## 🚀 How to Use the Reusable Prompt

See [`final_reusable_prompt.md`](./final_reusable_prompt.md) for the finalized template. You can copy the template directly into your IDE or LLM interface, populate the bracketed context blocks, and obtain production-ready, modular, and verified backend code in a single generation.
