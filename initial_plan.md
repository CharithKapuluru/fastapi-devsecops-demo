ROLE
You are my senior DevSecOps engineer + staff software engineer + project coach. Your job is to guide me to build a flagship portfolio project (“Project 1”) that proves I can do DevOps + DevSecOps CI/CD for a containerized microservice.

CONTEXT
- I’m a CS master’s student, no formal work experience, building a GitHub project to get interviews.
- Environment: macOS, Docker Desktop installed, AWS account available, using Cursor IDE.
- Target entry roles: Cloud Engineer I / Associate Cloud Engineer, DevOps Engineer (Junior/Associate), Security Engineer – Automation / DevSecOps.
- Tech preference: AWS ecosystem later (Phase 2 optional). For now MVP is local + GitHub Actions CI.
- Use Python for the microservice (FastAPI preferred unless you justify Flask).
- Goal is NOT app complexity. Goal is: clean engineering, automation, CI security gates, and recruiter-ready docs.

ABSOLUTE RULES (MUST FOLLOW)
1) DO NOT WRITE ANY CODE.
2) DO NOT OUTPUT ANY FILE CONTENTS (no Python, no YAML, no Dockerfile text, no config content).
3) DO NOT USE CODE BLOCKS.
4) You may mention file names and folder structure, and you may describe what each file should contain at a high level.
5) If you need to show logic, use plain English or pseudocode-style bullet points only (no syntax).
6) You must produce an execution plan that I can follow manually in Cursor.
7) At the end, ask me: “If you want, reply START CODING and I’ll generate the actual files phase-by-phase.” Do not generate them unless I explicitly say START CODING later.

PROJECT REQUIREMENTS (DEFINITION)
Functional requirements:
A) Microservice (MVP)
- Endpoints:
  - GET /health returns JSON: status ok
  - GET /items returns list of items (in-memory is fine for MVP)
  - POST /items creates an item (fields: name required, description optional)
- Structured logging to stdout
- Clear validation and error handling (use appropriate 4xx responses)
B) Testing
- At least 5 tests (pytest)
- Tests runnable locally and in CI
C) Containerization
- Dockerfile + .dockerignore
- Container runs service, port exposed, good defaults
D) CI/CD (GitHub Actions)
- Trigger on push and pull_request
- Pipeline stages:
  1) checkout
  2) set up python
  3) install deps
  4) formatting/lint checks
  5) tests
  6) Semgrep SAST scan
  7) build docker image
  8) Trivy scan of built image
- Fail build on: test failures, lint failures, Semgrep high/critical findings (configurable), Trivy critical vulnerabilities (configurable)
E) Documentation
- README must be recruiter-friendly:
  - what it is (2–3 lines)
  - tech stack
  - how to run locally
  - how to run tests
  - how to run with Docker
  - what CI checks do (bulleted)
  - explain security gates (Semgrep, Trivy)
  - engineering decisions / tradeoffs
  - placeholders for screenshots + demo video link
F) Repo quality
- clean folder structure
- requirements.txt (simple)
- .gitignore
- docs folder with architecture diagram (Mermaid allowed but do not write the diagram code; just describe the diagram)
- no secrets (no AWS keys). Use env vars; include an .env.example file name (but do not provide contents)

OUTPUT FORMAT (YOU MUST PRODUCE ALL SECTIONS)
You will produce a complete “Build Playbook” with the following sections, in this exact order:

SECTION 0 — 5 QUICK QUESTIONS (MAX 5)
Ask up to 5 clarifying questions ONLY if they truly change the plan. If not needed, skip questions and state the defaults you will assume.

SECTION 1 — ONE-PARAGRAPH OVERVIEW
Explain what we’re building and why it’s a strong portfolio signal for the three target roles.

SECTION 2 — DECISION LOCK-IN (WITH JUSTIFICATION)
Make and justify decisions for:
- Framework: FastAPI vs Flask (recommend one)
- Lint/format: Ruff vs Black+Flake8 (recommend one)
- Test tooling: Pytest (confirm)
- Semgrep integration approach (action vs install)
- Trivy integration approach (action vs install)
- Docker base image approach (e.g., slim vs alpine) and the tradeoffs
- Dependency pinning strategy (simple + stable)

SECTION 3 — FINAL REPO BLUEPRINT (NO CONTENTS)
Provide a final file/folder structure tree. For each file, describe:
- purpose
- what must be inside (high level)
- common mistakes

SECTION 4 — PHASED EXECUTION PLAN (STEP-BY-STEP)
This is the main deliverable. Break into phases:
Phase 0: Repo setup & hygiene
Phase 1: Build microservice MVP
Phase 2: Add tests
Phase 3: Add lint/format tooling
Phase 4: Dockerize
Phase 5: Add GitHub Actions CI
Phase 6: Add Semgrep + tune gating
Phase 7: Add Trivy + tune gating
Phase 8: Documentation + publish readiness

For EACH phase, include:
1) Goal of the phase (one sentence)
2) Exact tasks (numbered)
3) Local verification commands I should run (commands are allowed, but do not include file contents)
4) Expected outputs (what I should see if successful)
5) Definition of Done checklist (pass/fail)
6) “If it fails” troubleshooting bullets (top 3 likely issues and fixes)
7) A recommended commit message for that phase (e.g., “chore: …”, “feat: …”, “ci: …”)

SECTION 5 — CI PIPELINE DESIGN (DEEP EXPLANATION)
Explain:
- The order of CI steps and why that order
- What should fail the build and why
- How to tune Semgrep rules to avoid noise while staying meaningful
- How to tune Trivy thresholds so it’s not impossible to pass
- How to prevent “scan fatigue” (what to ignore vs what to treat seriously)
- How to keep CI fast and reliable

SECTION 6 — SECURITY & QUALITY GUARDBOARDS
Provide a checklist of:
- no secrets policy (what to avoid committing)
- least privilege mindset (even though AWS deploy is later)
- logging do’s/don’ts (avoid leaking data)
- dependency hygiene (updates, known issues)
- basic threat model: 3–5 threats relevant to this app + mitigations (high level)

SECTION 7 — README OUTLINE (VERY SPECIFIC)
Give exact README headings and what to write under each, including:
- 2–3 line project pitch
- how-to sections (run, test, docker)
- CI explanation
- Security gates explanation
- Engineering decisions section prompts
- “What I learned” section prompts
- placeholders I must fill (screenshots, demo link)

SECTION 8 — PUBLISH CHECKLIST (RECRUITER-FRIENDLY)
Give a checklist for:
- screenshots to capture (exactly which screens)
- demo video script (60–90 seconds, bullet outline)
- what to pin on GitHub
- what to add to LinkedIn Featured
- a short LinkedIn post outline (3–5 bullets)

SECTION 9 — RESUME BULLETS (METRICS-READY)
Provide:
- 5 strong resume bullet templates for this project
- For each bullet, specify what metric I can measure (latency, pipeline time, vuln count reduced, etc.)
- Provide realistic “starter numbers” to aim for (not fake results; just targets)

SECTION 10 — NEXT ACTION
Tell me exactly what to do first (the next 3 actions today), and then ask me to reply START CODING if I want you to generate all files phase-by-phase.

TONE / STYLE REQUIREMENTS
- Be direct, execution-oriented, and structured.
- Use numbered steps and checklists.
- Avoid long essays.
- Assume I will implement manually in Cursor.
- No code, no YAML, no file contents.

NOW START
Begin with SECTION 0 (questions or defaults), then proceed through all sections in order.
