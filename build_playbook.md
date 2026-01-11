# DevSecOps Portfolio Project - Complete Build Playbook

---

## SECTION 0 — 5 QUICK QUESTIONS (OR DEFAULTS)

I'm skipping the questions and declaring my defaults. Here's what I'm assuming:

**Default Assumptions:**
1. Project name will be "fastapi-devsecops-demo" (clean, searchable, descriptive)
2. Python version: 3.11 (stable, widely supported, good for resumes)
3. GitHub Actions: free tier is sufficient (no paid runners needed)
4. Security scan thresholds: Semgrep fails on HIGH/CRITICAL, Trivy fails on CRITICAL with unfixed vulns (tunable later)
5. No AWS deployment in this phase (local + Docker + CI only; AWS is future Phase 2)

---

## SECTION 1 — ONE-PARAGRAPH OVERVIEW

We're building a production-grade containerized Python microservice with a security-first CI/CD pipeline that demonstrates end-to-end DevSecOps skills. This project proves you can design clean REST APIs, write testable code, containerize services properly, automate quality gates (linting, testing), integrate SAST scanning (Semgrep), scan container images for vulnerabilities (Trivy), and document engineering decisions like a senior engineer. For Cloud Engineer roles, it shows infrastructure-as-code thinking and container fundamentals. For DevOps roles, it shows CI/CD automation and reliability practices. For DevSecOps roles, it proves you can shift security left with automated gates that catch issues before deployment. The entire project is recruiter-friendly: clear README, visual diagrams, demo-ready, and metric-driven resume bullets.

---

## SECTION 2 — DECISION LOCK-IN (WITH JUSTIFICATION)

**Framework: FastAPI (recommended)**
- Why: Automatic OpenAPI docs, built-in validation with Pydantic, async support, modern Python. Recruiters recognize it as cutting-edge. Flask is fine but FastAPI screams "I know modern stacks."
- Tradeoff: Slightly more opinionated than Flask, but that's good for portfolio projects (less boilerplate to write).

**Lint/Format: Ruff (recommended)**
- Why: 10-100x faster than Black+Flake8, all-in-one tool (linting + formatting), actively maintained, growing adoption. Simplifies CI.
- Tradeoff: Newer tool, but backed by Astral (creators of uv). Reduces tool sprawl vs managing Black+Flake8+isort.

**Test Tooling: Pytest (confirmed)**
- Why: Industry standard, clean syntax, great plugin ecosystem, excellent CI integration.
- No tradeoff: this is the default choice.

**Semgrep Integration: GitHub Action (recommended)**
- Why: Official Semgrep action is maintained, easy to configure, free for public repos, clear reporting.
- Tradeoff: Slightly less control vs manual install, but simpler for CI and automatically updates rules.

**Trivy Integration: Aqua Security Trivy Action (recommended)**
- Why: Official action, fast scans, outputs SARIF for GitHub Security tab integration, widely trusted.
- Tradeoff: Action abstracts some details, but provides cleaner CI YAML and automatic updates.

**Docker Base Image: python:3.11-slim (recommended)**
- Why: Balances size (smaller than full python image) and compatibility (more reliable than alpine). Debian-based, well-tested, fewer build issues.
- Tradeoff: Larger than alpine (~120MB vs ~50MB) but avoids musl libc issues and builds faster. For portfolio, reliability > extreme optimization.

**Dependency Pinning: Pragmatic pinning in requirements.txt (recommended)**
- Why: Reproducible builds, no surprise breakages in CI. Pin your direct dependencies (fastapi, uvicorn, pytest, ruff) to exact versions.
- Tradeoff: You can use pip freeze for everything, but it pins lots of transitive dependencies and can get messy. For portfolio projects, pinning only direct dependencies is cleaner and sufficient. Update monthly or when security issues arise.
- Practical approach: List main packages with exact versions, don't stress about every sub-dependency.

**Folder Naming: app/ instead of src/ (recommended)**
- Why: Using src/ often causes ModuleNotFoundError in tests and CI due to Python import path issues. Naming it app/ and importing as `from app.models import ...` is more straightforward and avoids path complications.
- Tradeoff: src/ is a common convention in some ecosystems, but for Python + FastAPI, app/ is cleaner and causes fewer beginner headaches.
- Decision: This playbook uses app/ throughout to prevent import frustration.

---

## 🚨 COMMON GOTCHAS (READ THIS FIRST)

These 5 fixes prevent 90% of frustration. The playbook incorporates them, but read this summary:

**A) Import Issues (FIXED)**
- Problem: src/ folders cause ModuleNotFoundError in tests/CI
- Solution: Using app/ instead of src/ throughout this playbook
- Benefit: Import as `from app.models import Item` - just works

**B) CI Security Tab Permissions (FIXED)**
- Problem: Semgrep/Trivy SARIF uploads silently fail without proper permissions
- Solution: Phase 5 adds `permissions: security-events: write` early
- Benefit: Security scan results actually appear in GitHub Security tab

**C) Trivy Base-Image Vulnerabilities (EXPECTED)**
- Problem: Trivy will flag 10-20 vulnerabilities in python:3.11-slim base image
- Reality: This is NORMAL. Debian packages have unfixable CVEs.
- Solution: Phase 7 configures fail-only-on-fixable-CRITICAL. Document the rest.
- Benefit: You won't panic when you see "15 vulnerabilities found"

**D) Dependency Pinning (PRAGMATIC)**
- Problem: `pip freeze` creates messy requirements.txt with 50+ transitive deps
- Solution: Pin only direct dependencies (fastapi==X.X.X, uvicorn==X.X.X, pytest==X.X.X, ruff==X.X.X)
- Benefit: Clean, maintainable requirements.txt that's good enough for portfolio

**E) Quality of Life Commands (ADDED)**
- Problem: Recruiters/reviewers want easy commands like `make run`, `make test`
- Solution: Phase 1 includes creating a Makefile with common targets
- Benefit: Repo feels professional with almost no extra work

---

## SECTION 3 — FINAL REPO BLUEPRINT (NO CONTENTS)

Here's your final folder structure:

```
fastapi-devsecops-demo/
├── .github/
│   └── workflows/
│       └── ci.yml
├── docs/
│   └── architecture.md
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   └── config.py
├── tests/
│   ├── __init__.py
│   └── test_api.py
├── .dockerignore
├── .env.example
├── .gitignore
├── Dockerfile
├── Makefile
├── README.md
└── requirements.txt
```

**File Descriptions:**

**.github/workflows/ci.yml**
- Purpose: GitHub Actions workflow definition for CI/CD pipeline
- Must contain: Trigger config (push/PR), jobs for lint/test/scan/build, Semgrep step, Trivy step, failure conditions
- Common mistakes: Running scans before tests (wastes time), not caching Python deps, unclear failure messages

**docs/architecture.md**
- Purpose: Architecture diagram and system design explanation
- Must contain: Component diagram (can use Mermaid), request flow explanation, security boundaries, future scaling notes
- Common mistakes: Over-complicating for a simple service, not explaining why choices were made

**app/__init__.py**
- Purpose: Makes app a package
- Must contain: Can be empty or contain version string
- Common mistakes: Adding unnecessary imports that create circular dependencies

**app/main.py**
- Purpose: FastAPI application definition and route handlers
- Must contain: App initialization, health endpoint, items endpoints (GET/POST), logging setup, error handlers
- Common mistakes: Mixing business logic with routes, no input validation, missing error handling

**app/models.py**
- Purpose: Pydantic models for request/response validation
- Must contain: Item model with name (required) and description (optional), response models
- Common mistakes: Weak validation, missing example data for docs, not using Pydantic properly

**app/config.py**
- Purpose: Configuration management (env vars, constants)
- Must contain: Logging config, environment variable loading, app settings
- Common mistakes: Hardcoding values, no defaults, exposing secrets

**tests/__init__.py**
- Purpose: Makes tests a package
- Must contain: Can be empty or shared fixtures
- Common mistakes: None really, just don't forget it

**tests/test_api.py**
- Purpose: API endpoint tests
- Must contain: At least 5 tests covering health check, GET items (empty/with data), POST valid item, POST invalid item, error cases
- Common mistakes: Not using TestClient properly, no cleanup between tests, weak assertions

**.dockerignore**
- Purpose: Exclude files from Docker build context
- Must contain: Entries for tests, docs, .git, __pycache__, .env, *.md (except essential ones)
- Common mistakes: Forgetting this file (bloats image), not excluding .git (security risk)

**.env.example**
- Purpose: Template showing required environment variables
- Must contain: List of env var names with dummy values and comments explaining each
- Common mistakes: Including actual secrets, unclear variable names

**.gitignore**
- Purpose: Exclude files from Git
- Must contain: __pycache__, .env, .pytest_cache, .ruff_cache, *.pyc, .DS_Store, venv/
- Common mistakes: Not covering Python artifacts, forgetting OS-specific files

**Dockerfile**
- Purpose: Container image build instructions
- Must contain: FROM python:3.11-slim, WORKDIR, COPY requirements.txt, RUN pip install, COPY app, EXPOSE port, CMD to run app
- Common mistakes: Running as root, copying unnecessary files, not using layer caching properly, no health check

**Makefile**
- Purpose: Quality-of-life command runner for common tasks
- Must contain: Targets for run, test, lint, format, docker-build, docker-run (makes repo feel professional with almost no work)
- Common mistakes: Over-complicating it, forgetting .PHONY declarations, not testing commands

**README.md**
- Purpose: Main project documentation (recruiter-facing)
- Must contain: Project pitch, tech stack badge/list, setup instructions, test instructions, Docker instructions, CI explanation, security gates, decisions, placeholders for screenshots/video
- Common mistakes: Too technical, no visuals, missing "why" explanations, looks like toy project

**requirements.txt**
- Purpose: Python dependencies
- Must contain: fastapi, uvicorn[standard], pydantic, pytest, httpx (for testing), ruff - all pinned to exact versions (e.g., fastapi==0.104.1)
- Common mistakes: Not pinning versions, using `pip freeze` and getting 50+ transitive deps (keep it simple, pin only direct dependencies), missing test dependencies

---

## SECTION 4 — PHASED EXECUTION PLAN (STEP-BY-STEP)

### PHASE 0: Repo Setup & Hygiene

**Goal:** Create clean repo foundation with proper Git hygiene

**Exact Tasks:**
1. Create new directory fastapi-devsecops-demo on your machine
2. Initialize Git repository
3. Create .gitignore file with Python-specific exclusions
4. Create initial README.md with project title and "Work in Progress" note
5. Create folder structure: app/, tests/, docs/, .github/workflows/
6. Make initial commit
7. Create GitHub repository (public)
8. Push to GitHub

**Local Verification Commands:**
- git status (should show clean working tree)
- ls -la (verify folder structure exists)
- git log (should show initial commit)

**Expected Outputs:**
- Folder structure matches blueprint
- Git repository initialized locally and on GitHub
- Clean git status

**Definition of Done:**
- [ ] Folders created: app, tests, docs, .github/workflows
- [ ] .gitignore exists with Python entries
- [ ] README.md exists
- [ ] Initial commit made
- [ ] GitHub repo created and linked
- [ ] git remote -v shows GitHub URL

**If It Fails (Top 3 Issues):**
1. Git not installed: Install Git via Homebrew (brew install git)
2. GitHub authentication fails: Set up SSH keys or use GitHub CLI (gh auth login)
3. Folder permissions issue: Check you have write access to Desktop/Proj-1

**Recommended Commit Message:**
```
chore: initialize project structure and Git repository
```

---

### PHASE 1: Build Microservice MVP

**Goal:** Create working FastAPI service with health and items endpoints

**Exact Tasks:**
1. Create app/__init__.py (empty file)
2. Create app/config.py with logging configuration
3. Create app/models.py with Item Pydantic model
4. Create app/main.py with FastAPI app, health endpoint, items endpoints (GET/POST)
5. Create requirements.txt with fastapi and uvicorn dependencies (pin to specific versions)
6. Create Makefile with basic targets (run, test, lint, docker-build, docker-run)
7. Install dependencies in virtual environment
8. Run the service locally
9. Test endpoints manually with browser or curl

**Local Verification Commands:**
- python3 -m venv venv
- source venv/bin/activate
- pip install -r requirements.txt
- uvicorn app.main:app --reload (or make run if you created Makefile first)
- curl http://localhost:8000/health
- curl http://localhost:8000/items
- curl -X POST http://localhost:8000/items -H "Content-Type: application/json" -d '{"name":"test"}'

**Expected Outputs:**
- Server starts on port 8000
- GET /health returns {"status":"ok"}
- GET /items returns empty list or items
- POST /items creates item and returns it
- Logs appear in terminal with structured format

**Definition of Done:**
- [ ] FastAPI app runs without errors
- [ ] All 3 endpoints respond correctly
- [ ] Logging outputs to stdout
- [ ] Input validation works (POST with missing name should fail)
- [ ] Can access OpenAPI docs at /docs

**If It Fails (Top 3 Issues):**
1. Import errors: Check virtual environment is activated, check file structure matches imports
2. Port already in use: Kill process on 8000 or use --port 8001
3. Module not found: Ensure you're running from project root, check PYTHONPATH

**Recommended Commit Message:**
```
feat: implement FastAPI microservice with health and items endpoints
```

---

### PHASE 2: Add Tests

**Goal:** Achieve test coverage with pytest for all endpoints

**Exact Tasks:**
1. Add pytest and httpx to requirements.txt
2. Create tests/__init__.py (empty)
3. Create tests/test_api.py with TestClient setup
4. Write test for GET /health
5. Write test for GET /items (empty state)
6. Write test for POST /items (valid data)
7. Write test for POST /items (invalid data - missing name)
8. Write test for GET /items (after adding items)
9. Run tests locally

**Local Verification Commands:**
- pip install -r requirements.txt
- pytest tests/ -v (or make test)
- pytest tests/ --cov=app (if you add pytest-cov, optional)

**Expected Outputs:**
- All 5+ tests pass
- Clear test names and output
- No warnings or errors
- Tests complete in under 2 seconds

**Definition of Done:**
- [ ] At least 5 tests written
- [ ] All tests pass locally
- [ ] Tests cover happy path and error cases
- [ ] Tests are isolated (no shared state issues)
- [ ] pytest runs cleanly with no warnings

**If It Fails (Top 3 Issues):**
1. TestClient import fails: Ensure httpx is installed (fastapi test dependency)
2. Tests fail due to shared state: Use fresh app instance or reset data between tests
3. Import errors in tests: Check relative imports, ensure running from project root

**Recommended Commit Message:**
```
test: add pytest suite with coverage for all endpoints
```

---

### PHASE 3: Add Lint/Format Tooling

**Goal:** Add Ruff for code quality and formatting checks

**Exact Tasks:**
1. Add ruff to requirements.txt
2. Create pyproject.toml for Ruff configuration
3. Configure Ruff with line length, basic rules, exclude patterns
4. Run ruff check on app/ and tests/
5. Fix any issues found
6. Run ruff format to auto-format code
7. Re-run tests to ensure formatting didn't break anything

**Local Verification Commands:**
- pip install -r requirements.txt
- ruff check app/ tests/ (or make lint)
- ruff format app/ tests/ (or make format)
- pytest tests/ -v (or make test)

**Expected Outputs:**
- Ruff check shows no errors
- Code is formatted consistently
- Tests still pass after formatting
- Clear output showing files checked

**Definition of Done:**
- [ ] Ruff installed and configured
- [ ] ruff check passes with no errors
- [ ] Code is formatted
- [ ] pyproject.toml exists with Ruff config
- [ ] Tests still pass

**If It Fails (Top 3 Issues):**
1. Ruff finds many issues: Run ruff format first to auto-fix, then address remaining issues
2. Configuration errors: Check pyproject.toml syntax (use TOML format)
3. Conflicts with existing code: Adjust Ruff rules to be less strict initially, tighten later

**Recommended Commit Message:**
```
chore: add Ruff for linting and formatting with configuration
```

---

### PHASE 4: Dockerize

**Goal:** Create production-ready container image

**Exact Tasks:**
1. Create .dockerignore file
2. Create Dockerfile with simple single-stage build
3. Verify requirements.txt has pinned versions for main dependencies (fastapi, uvicorn, pytest, ruff with ==X.X.X)
4. Build Docker image locally
5. Run container locally
6. Test endpoints on running container
7. Verify logs appear correctly
8. Stop and remove container

**Local Verification Commands:**
- docker build -t fastapi-devsecops-demo:latest . (or make docker-build)
- docker run -d -p 8000:8000 --name test-api fastapi-devsecops-demo:latest (or make docker-run)
- curl http://localhost:8000/health
- docker logs test-api
- docker stop test-api && docker rm test-api

**Expected Outputs:**
- Image builds successfully (under 2 minutes)
- Container starts and responds to requests
- Logs visible via docker logs
- Image size reasonable (under 300MB)

**Definition of Done:**
- [ ] Dockerfile exists and follows best practices
- [ ] .dockerignore exists
- [ ] Image builds without errors
- [ ] Container runs and serves traffic
- [ ] requirements.txt has pinned versions
- [ ] No unnecessary files in image (check with docker exec)

**If It Fails (Top 3 Issues):**
1. Build fails on pip install: Check requirements.txt format, ensure no Windows line endings
2. Container exits immediately: Check CMD is correct, review logs with docker logs
3. Can't reach endpoints: Ensure EXPOSE and -p port mapping match, check app binds to 0.0.0.0 not localhost

**Recommended Commit Message:**
```
feat: add Dockerfile and containerize application
```

---

### PHASE 5: Add GitHub Actions CI

**Goal:** Automate testing and linting on every push/PR

**Exact Tasks:**
1. Create .github/workflows/ci.yml
2. Configure workflow triggers (push to main, pull requests)
3. Add job with steps: checkout, setup Python 3.11, install deps, run Ruff, run pytest
4. Configure dependency caching for faster runs
5. Add permissions block (needed later for Security tab uploads): permissions: contents: read, security-events: write
6. Push to GitHub
7. Verify workflow runs and passes
8. Intentionally break a test, push, verify CI fails
9. Fix test, verify CI passes again

**CRITICAL NOTE:** The permissions: security-events: write is required for Semgrep/Trivy SARIF uploads to appear in the GitHub Security tab. Add this early to avoid silent upload failures later.

**Local Verification Commands:**
- git add .github/workflows/ci.yml
- git commit -m "ci: add GitHub Actions workflow"
- git push origin main
- (Check GitHub Actions tab in browser)

**Expected Outputs:**
- Workflow appears in GitHub Actions tab
- All steps complete successfully (green checkmarks)
- Workflow completes in under 3 minutes
- Failed tests cause workflow to fail (verify with test break)

**Definition of Done:**
- [ ] ci.yml exists in .github/workflows/
- [ ] Workflow triggers on push and PR
- [ ] All steps execute in correct order
- [ ] Workflow passes on clean code
- [ ] Workflow fails when tests fail
- [ ] Python dependencies are cached

**If It Fails (Top 3 Issues):**
1. YAML syntax errors: Use YAML validator, check indentation (spaces not tabs)
2. Workflow doesn't trigger: Check branch name matches, verify GitHub Actions enabled in repo settings
3. Tests fail in CI but pass locally: Check Python version matches, review environment differences

**Recommended Commit Message:**
```
ci: implement GitHub Actions workflow for automated testing and linting
```

---

### PHASE 6: Add Semgrep + Tune Gating

**Goal:** Integrate SAST scanning with appropriate failure thresholds

**Exact Tasks:**
1. Add Semgrep step to ci.yml workflow using official action
2. Configure to scan app/ directory
3. Set initial policy: fail on HIGH and CRITICAL findings
4. Ensure SARIF upload is configured (should work automatically if permissions set in Phase 5)
5. Push and let workflow run
6. Review any findings in GitHub Security tab
7. If false positives exist, create .semgrepignore or adjust rules
8. Document decision to ignore specific findings in docs/
9. Ensure workflow still fails on legitimate issues (test with intentional vulnerability if needed)

**Local Verification Commands:**
- git add .github/workflows/ci.yml
- git commit -m "ci: add Semgrep SAST scanning"
- git push origin main
- (Check GitHub Actions tab and Security tab)

**Expected Outputs:**
- Semgrep step runs in CI
- SARIF results uploaded to GitHub Security tab
- No HIGH/CRITICAL findings in clean code
- Workflow completes successfully if no issues

**Definition of Done:**
- [ ] Semgrep action added to workflow
- [ ] Scans complete without errors
- [ ] Results visible in GitHub Security tab
- [ ] Failure threshold configured (HIGH/CRITICAL)
- [ ] No false positives blocking builds
- [ ] Real issues would fail the build

**If It Fails (Top 3 Issues):**
1. Semgrep finds issues: Review findings, fix real issues, ignore false positives via .semgrepignore
2. Action configuration errors: Check action version, review Semgrep action docs for correct syntax
3. Uploads fail to Security tab: Ensure SARIF format enabled, check repo permissions for SARIF upload

**Recommended Commit Message:**
```
ci: integrate Semgrep SAST scanning with security gating
```

---

### PHASE 7: Add Trivy + Tune Gating

**Goal:** Scan Docker images for vulnerabilities with sensible thresholds

**⚠️ EXPECTATION MANAGEMENT:** Trivy will almost certainly flag vulnerabilities in the python:3.11-slim base image (Debian packages). This is NORMAL. Even "clean" base images have unfixable vulnerabilities from underlying OS packages. Don't panic. The goal is to fail only on CRITICAL vulnerabilities that have available fixes in YOUR dependencies, not every base-image CVE.

**Exact Tasks:**
1. Add Docker build step to ci.yml (before Trivy)
2. Add Trivy scanning step using Aqua Security action
3. Configure to scan built image
4. Set severity threshold: fail on CRITICAL with fix available (use exit-code and severity flags)
5. Configure SARIF upload for GitHub Security tab (should work if permissions set in Phase 5)
6. Push and let workflow run
7. Review vulnerability report - expect to see MEDIUM/HIGH findings in base image
8. If unfixable CRITICAL vulns exist in base image, document acceptance decision in README and adjust threshold if needed
9. Verify scan results are readable and actionable

**REALITY CHECK:** If Trivy shows 10-20 MEDIUM/HIGH findings in Debian packages, that's normal. Focus on CRITICAL with fixes in your Python packages (fastapi, uvicorn, etc.), not OS-level stuff you can't control.

**Local Verification Commands:**
- git add .github/workflows/ci.yml
- git commit -m "ci: add Trivy container scanning"
- git push origin main
- (Check GitHub Actions and Security tab)
- (Optionally run Trivy locally: docker run aquasec/trivy image fastapi-devsecops-demo:latest)

**Expected Outputs:**
- Docker image builds in CI
- Trivy scan completes
- Vulnerability report available
- Workflow passes if no fixable CRITICAL vulns
- SARIF uploaded to Security tab

**Definition of Done:**
- [ ] Docker build step added to workflow
- [ ] Trivy action configured correctly
- [ ] Scan runs on built image
- [ ] Threshold set appropriately (documented)
- [ ] Results in GitHub Security tab
- [ ] No fixable critical vulnerabilities
- [ ] Scan time is reasonable (under 2 minutes)

**If It Fails (Top 3 Issues):**
1. Trivy finds unfixable vulns in base image: THIS IS EXPECTED. Document in README's Engineering Decisions section, explain these are Debian base-image CVEs with no fixes available. Adjust threshold or use ignore rules if needed. This is normal and acceptable for portfolio projects.
2. Scan takes too long: Trivy should be fast (under 2 min), but check for network issues or large image size
3. SARIF upload fails: Verify permissions: security-events: write was set in Phase 5. Check action configuration.

**Recommended Commit Message:**
```
ci: add Trivy vulnerability scanning for container images
```

---

### PHASE 8: Documentation + Publish Readiness

**Goal:** Create recruiter-ready documentation and visuals

**Exact Tasks:**
1. Complete README.md with all required sections (see Section 7)
2. Create docs/architecture.md with system diagram description (Mermaid optional)
3. Take screenshots: CI passing, Security tab with scans, OpenAPI docs, running container logs
4. Create .env.example with placeholder values
5. Record demo video (60-90 seconds) showing: local run, test execution, Docker build, API call, CI dashboard
6. Add demo video link to README
7. Add screenshots to docs/ or embed in README
8. Review entire README as if you're a recruiter
9. Final proofread for typos and clarity
10. Push final version

**Local Verification Commands:**
- Open README.md and review each section
- Check all links work
- Verify images display correctly
- Spell check document

**Expected Outputs:**
- README is complete, clear, professional
- All placeholders filled
- Screenshots are high-quality and relevant
- Demo video is concise and shows key features
- Documentation explains WHY not just WHAT

**Definition of Done:**
- [ ] README has all sections from Section 7
- [ ] Architecture diagram described or included
- [ ] Screenshots added (minimum 3)
- [ ] Demo video recorded and linked
- [ ] .env.example created
- [ ] No TODOs or placeholders remain
- [ ] Spelling and grammar checked
- [ ] Links tested

**If It Fails (Top 3 Issues):**
1. Video recording issues: Use QuickTime (macOS) or OBS, keep it simple, focus on showing not telling
2. Screenshots unclear: Use high resolution, highlight important parts, add captions
3. README too long: Cut fluff, keep it scannable with headers and bullets

**Recommended Commit Message:**
```
docs: complete README and architecture documentation with visuals
```

---

## SECTION 5 — CI PIPELINE DESIGN (DEEP EXPLANATION)

**Order of CI Steps and Rationale:**

1. **Checkout code** - Must be first, nothing else can run without code
2. **Setup Python** - Needed for all subsequent Python operations
3. **Install dependencies** - Required before running any tools
4. **Ruff linting/formatting** - Fast, catches obvious issues early, fails fast (under 10 seconds)
5. **Run tests** - Validates functionality, should happen before expensive operations (under 30 seconds)
6. **Semgrep SAST scan** - Checks code quality/security before building artifacts (under 1 minute)
7. **Build Docker image** - Creates artifact only after code quality confirmed (1-2 minutes)
8. **Trivy image scan** - Scans the built artifact for vulnerabilities (under 1 minute)

**Why This Order:**
- Fast feedback first (lint before tests before scans)
- Don't waste time building Docker images if code doesn't work
- Catch cheap-to-fix issues (formatting) before expensive-to-fix issues (security vulns)
- Build artifacts only once quality gates pass

**What Should Fail the Build:**

1. **Linting failures** - Code doesn't meet quality standards
2. **Test failures** - Broken functionality
3. **Semgrep HIGH/CRITICAL** - Serious code security/quality issues
4. **Trivy CRITICAL (fixable)** - Known vulnerabilities with available patches
5. **Build failures** - Docker image won't build

**What Should NOT Fail the Build (Initially):**
- Semgrep LOW/MEDIUM findings (warn only, create issues to track)
- Trivy MEDIUM/HIGH findings (log and monitor trends)
- Trivy CRITICAL unfixable (document and accept risk if in base image dependencies)

**Tuning Semgrep:**

Start conservative, tighten over time:
- **Phase 1:** Use Semgrep's "auto" or "recommended" ruleset, fail on HIGH/CRITICAL only
- **Phase 2:** Review findings, create nosemgrep comments for false positives with justification
- **Phase 3:** Add custom rules if you find patterns specific to your code
- **Avoid noise:** Don't enable every ruleset, focus on security and reliability rules
- **Document decisions:** If you suppress a finding, explain why in code comments or docs

Example suppression approach:
- False positive: Add inline nosemgrep comment with brief reason
- Accepted risk: Document in docs/security-decisions.md
- Will fix later: Create GitHub issue, link in comment

**Tuning Trivy:**

Balance security with practicality:
- **Start:** Fail on CRITICAL with fixes available
- **Middle ground:** Track HIGH, review regularly, fix when feasible
- **Reality check:** Some base image vulns have no fix - document and accept or choose different base image
- **Regular updates:** Run dependency updates monthly, re-scan
- **Ignore noise:** Use .trivyignore for known false positives (rare) with justification

Example threshold progression:
- Week 1: Fail on CRITICAL, warn on HIGH
- Month 1: Fix most HIGH, keep failing on CRITICAL
- Month 3: Consider failing on HIGH if staying on top of updates

**Preventing Scan Fatigue:**

Scan fatigue happens when too many findings create noise and teams ignore results. Prevent this:

1. **Start strict but realistic** - Don't fail on everything, you'll ignore failures
2. **Triage immediately** - Fix, ignore with reason, or accept and document - never let findings accumulate
3. **Automate what you can** - Use dependabot or Renovate for dependency updates
4. **Review trends not absolutes** - Are vulns increasing or decreasing over time?
5. **Make scans fast** - Slow CI means developers avoid running it
6. **Clear ownership** - Someone must review security findings weekly

**Treat seriously:**
- Any CRITICAL finding with a fix available
- HIGH findings in your code (not dependencies)
- Repeated patterns (same issue in multiple places)
- Exploitable vulns with known CVEs

**Ignore safely:**
- LOW findings unless they're easy fixes
- Unfixable dependency issues (if you've documented why you can't upgrade)
- False positives (but verify they're actually false)

**Keep CI Fast and Reliable:**

Target: Under 5 minutes total CI time

Speed optimizations:
- **Cache dependencies** - GitHub Actions cache for pip packages (saves 30-60 seconds)
- **Cache Docker layers** - Use Docker BuildKit and layer caching
- **Parallel jobs** - Run lint and test in parallel if no dependencies
- **Fail fast** - Put fastest checks first so you find out quickly
- **Right-size runners** - GitHub free runners are fine for this project

Reliability:
- **Pin action versions** - Use @v3 not @latest to avoid surprise breakages
- **Pin Python version** - Specify exact version (3.11.5 not just 3.11)
- **Avoid flaky tests** - No sleeps, no external API calls in tests
- **Clear error messages** - When CI fails, error should be obvious

---

## SECTION 6 — SECURITY & QUALITY GUARDRAILS

**No Secrets Policy:**

Never commit these:
- API keys, tokens, passwords
- AWS credentials or access keys
- Private keys or certificates
- Database connection strings with credentials
- .env files with real values
- Any hardcoded secrets in code

Safe practices:
- Use environment variables for all secrets
- Provide .env.example with dummy values
- Add .env to .gitignore
- Use descriptive env var names (AWS_ACCESS_KEY_ID not KEY)
- Document all required env vars in README
- If you accidentally commit a secret: rotate it immediately, don't just delete from Git (history persists)

**Least Privilege Mindset:**

Even though AWS deployment is Phase 2, build with least privilege now:
- Container runs as non-root user (add USER directive in Dockerfile)
- No unnecessary file permissions in Docker COPY
- No overly broad CORS policies (restrict origins)
- Log what you need, not everything
- Don't expose internal error details to API responses (use generic messages)

Future AWS prep:
- Use IAM roles, not access keys
- Each service gets minimum permissions needed
- No wildcard permissions (*)

**Logging Do's and Don'ts:**

DO:
- Log request IDs for traceability
- Log errors with context (what failed, when, where)
- Use structured logging (JSON format)
- Log security events (auth failures, invalid input)
- Include timestamps and log levels

DON'T:
- Log passwords or tokens
- Log full request bodies that might contain PII
- Log sensitive query parameters
- Log full credit card numbers or SSNs
- Over-log (creates noise and storage costs)

Example of safe logging approach:
- Log: "User authentication failed for user_id=123"
- Don't log: "Login failed with password=hunter2"

**Dependency Hygiene:**

Practices to follow:
- Pin exact versions for direct dependencies in requirements.txt (e.g., fastapi==0.104.1)
- You CAN use `pip freeze` but it's messy (pins 50+ transitive deps). For portfolio, pinning only your direct 5-6 dependencies is cleaner and sufficient.
- Review dependencies before adding (check download count, last update, license)
- Update dependencies monthly or when security issues found
- Run pip-audit or similar tool to check for known vulnerabilities
- Keep dependencies minimal (don't add libraries you don't need)
- Document why each major dependency is needed

Workflow:
1. Add dependency with specific version (e.g., fastapi==0.104.1)
2. Test thoroughly
3. Commit requirements.txt with pinned version
4. Document in requirements.txt with comment if non-obvious
5. Monthly: check for updates, test, update pins

**Pragmatic Note:** If you're torn between "pip freeze everything" vs "pin only direct deps," choose the latter for portfolio projects. It's cleaner, easier to maintain, and just as professional.

**Basic Threat Model:**

For this application, consider these threats and mitigations:

**Threat 1: Code Injection via /items POST**
- Risk: User sends malicious JSON that gets executed or stored unsafely
- Mitigation: Pydantic validation, no eval/exec, escape any output, input length limits
- Residual risk: Low if using Pydantic properly

**Threat 2: Dependency Vulnerabilities**
- Risk: Using libraries with known security flaws
- Mitigation: Trivy scans, regular updates, monitoring security advisories
- Residual risk: Medium (always some lag between disclosure and fixes)

**Threat 3: Container Escape or Privilege Escalation**
- Risk: Attacker breaks out of container or gains root access
- Mitigation: Run as non-root user, minimal base image, regular image updates
- Residual risk: Low for this simple app, higher if deploying to multi-tenant environments

**Threat 4: Denial of Service (DoS)**
- Risk: Attacker floods API with requests, crashes service
- Mitigation: Rate limiting (add later), resource limits in Docker, input size limits
- Residual risk: Medium (no rate limiting in MVP)

**Threat 5: Information Disclosure**
- Risk: Error messages or logs reveal system details
- Mitigation: Generic error messages to clients, don't expose stack traces, careful logging
- Residual risk: Low if following logging guidelines

For each threat, document: what it is, how likely, impact if exploited, current mitigations, and future improvements.

---

## SECTION 7 — README OUTLINE (VERY SPECIFIC)

Your README.md should have these exact sections:

**Section: Project Title and Badges**
- Project name as H1
- Badges for: Build Status (GitHub Actions), Python version, License
- One-line tagline: "Production-ready FastAPI microservice with security-first CI/CD"

**Section: Overview (2-3 lines)**
What to write:
- One sentence: what the service does (REST API for managing items)
- One sentence: what the project demonstrates (DevSecOps practices, automated security gates, container best practices)
- One sentence: who it's for (portfolio project for Cloud/DevOps/DevSecOps roles)

**Section: Tech Stack**
Provide bulleted list:
- Backend: FastAPI, Python 3.11, Pydantic
- Testing: Pytest
- Code Quality: Ruff (linting + formatting)
- Containerization: Docker (python:3.11-slim base)
- CI/CD: GitHub Actions
- Security: Semgrep (SAST), Trivy (container scanning)

**Section: Features**
Bullet points of what works:
- RESTful API with three endpoints
- Input validation and error handling
- Structured logging
- Comprehensive test suite
- Automated CI/CD pipeline
- Security scanning integration
- Production-ready containerization

**Section: Getting Started**
Three subsections:

**Subsection: Prerequisites**
- Python 3.11+
- Docker (optional, for container testing)
- Git

**Subsection: Local Setup**
Step-by-step:
1. Clone the repository
2. Create virtual environment
3. Install dependencies
4. Run the application
5. Access API docs at localhost:8000/docs

Include exact commands but no file contents.

**Subsection: Running Tests**
- Command to run tests
- Expected output
- How to run with coverage (if implemented)

**Section: Docker Usage**
Three subsections:

**Subsection: Build Image**
- Command to build
- Expected output (success message)

**Subsection: Run Container**
- Command to run with port mapping
- How to verify it's running
- How to view logs

**Subsection: Stop Container**
- Commands to stop and remove

**Section: CI/CD Pipeline**
Explain what happens on every push:

1. Code checkout
2. Linting and formatting checks (Ruff)
3. Test suite execution
4. SAST scanning with Semgrep
5. Docker image build
6. Container vulnerability scanning with Trivy

State: "All checks must pass before merging to main"

**Section: Security Gates**
Two subsections:

**Subsection: Semgrep SAST**
- What it scans for (code quality, security patterns)
- Failure threshold (HIGH/CRITICAL)
- Where to view results (GitHub Security tab)

**Subsection: Trivy Container Scanning**
- What it scans for (OS and library vulnerabilities)
- Failure threshold (CRITICAL with fixes)
- How findings are tracked

**Section: Engineering Decisions**
Document your key choices with brief rationale:
- Why FastAPI over Flask
- Why Ruff over Black+Flake8
- Why python:3.11-slim over alpine
- Why these specific security thresholds
- Any tradeoffs made

Format: Decision -> Rationale -> Tradeoff (one paragraph each)

**Section: Project Structure**
Show your folder tree (no file contents, just structure)
Brief description of each major directory's purpose

**Section: What I Learned**
Reflective section for recruiting conversations:
- Technical skills gained
- Challenges faced and how you solved them
- What you'd do differently next time
- What you're proud of

Prompts:
- "Implementing Semgrep taught me..."
- "The biggest challenge was... I solved it by..."
- "If I rebuilt this, I would..."
- "I'm particularly proud of..."

**Section: Demo and Visuals**
- Link to demo video (YouTube or Loom)
- Screenshot of CI passing
- Screenshot of OpenAPI docs
- Screenshot of Security tab with scan results

**Section: Future Enhancements**
Bullet list of Phase 2 ideas:
- AWS deployment (ECS or EKS)
- Terraform for infrastructure
- CloudWatch integration
- Rate limiting
- Database integration
- Authentication/authorization

**Section: License**
- MIT License (standard for portfolio projects)

**Section: Contact**
- Your name
- LinkedIn profile
- GitHub profile
- Optional: portfolio website

---

## SECTION 8 — PUBLISH CHECKLIST (RECRUITER-FRIENDLY)

**Screenshots to Capture:**

1. **GitHub Actions Dashboard (CI Passing)**
   - Where: GitHub repo -> Actions tab
   - What: Workflow run with all green checkmarks
   - Highlight: Show all steps passed, include timestamp

2. **OpenAPI Documentation**
   - Where: localhost:8000/docs while app is running
   - What: Full Swagger UI showing all endpoints
   - Highlight: Shows professional API design

3. **Security Tab with Scan Results**
   - Where: GitHub repo -> Security tab -> Code scanning alerts
   - What: Semgrep and Trivy results (ideally showing no critical findings)
   - Highlight: Demonstrates security practices

4. **Running Container Logs**
   - Where: Terminal with docker logs command output
   - What: Structured JSON logs showing requests being processed
   - Highlight: Production-ready logging

5. **Test Execution Output**
   - Where: Terminal with pytest output
   - What: All tests passing with clear names
   - Highlight: Test coverage and quality

**Demo Video Script (60-90 seconds):**

Introduction (10 sec):
- "This is a production-grade FastAPI microservice demonstrating DevSecOps best practices"

Show Local Run (15 sec):
- Run uvicorn command
- Open browser to /docs
- Show API endpoints

Show Testing (10 sec):
- Run pytest command
- Show all tests passing

Show Docker (15 sec):
- Build image (show command, mention fast build)
- Run container
- Make API call with curl

Show CI/CD (20 sec):
- Open GitHub Actions tab
- Walk through pipeline stages
- Highlight security scans
- Show all passing

Show Security (15 sec):
- Open GitHub Security tab
- Show Semgrep results
- Show Trivy results
- Mention zero critical findings

Closing (5 sec):
- "Full code and documentation on GitHub"
- Show GitHub repo URL

**What to Pin on GitHub:**

1. Pin this repository to your profile
2. Add topics/tags: fastapi, devsecops, cicd, docker, python, github-actions, semgrep, trivy, portfolio
3. Ensure description is clear: "Production-ready FastAPI microservice with automated security scanning and CI/CD"
4. Add website link (if you have portfolio site)

**What to Add to LinkedIn Featured:**

1. Link to GitHub repository
   - Title: "DevSecOps Portfolio Project - FastAPI Microservice"
   - Description: "Demonstrates CI/CD automation, SAST scanning, container security, and production best practices"

2. Link to demo video
   - Title: "Project Demo - Secure CI/CD Pipeline"
   - Description: "90-second walkthrough of automated testing and security gates"

3. Architecture diagram (if you export as image)
   - Title: "System Architecture"

**LinkedIn Post Outline (3-5 bullets):**

Opening hook:
"Just shipped a production-grade DevSecOps portfolio project I'm excited to share!"

What you built:
- FastAPI microservice with automated security scanning
- Complete CI/CD pipeline with Semgrep SAST and Trivy vulnerability scanning
- Containerized with Docker, tested with pytest, all in GitHub Actions

What you learned:
- How to integrate security gates into CI/CD without breaking developer velocity
- Balancing security strictness with practical deployment needs
- Building production-ready APIs with proper validation and error handling

The metrics:
- X tests with 100% passing rate
- CI pipeline completes in under 5 minutes
- Zero critical security findings

Call to action:
- "Check out the code and demo video [link]"
- "Would love feedback from DevOps/Security engineers on the approach!"

Hashtags: #DevSecOps #CloudEngineering #DevOps #Python #FastAPI #Docker #CICD

---

## SECTION 9 — RESUME BULLETS (METRICS-READY)

Here are 5 resume bullet templates with measurement guidance:

**Bullet 1: CI/CD Automation**
Template: "Designed and implemented automated CI/CD pipeline using GitHub Actions, reducing deployment validation time by X% through parallel execution of linting, testing, and security scanning stages"

Metric to measure: Time from local test run + manual docker build + manual scan vs automated pipeline
Realistic starter: 70-80% reduction (manual might take 10-15 min, automated 2-5 min)

**Bullet 2: Security Integration**
Template: "Integrated Semgrep SAST and Trivy container scanning into CI pipeline, catching X security vulnerabilities before production and establishing automated security gates for all code changes"

Metric to measure: Count findings during development (check Semgrep/Trivy reports)
Realistic starter: 5-15 findings caught (LOW/MEDIUM issues count, even if you fixed them)

**Bullet 3: Container Optimization**
Template: "Containerized Python microservice using Docker with optimized multi-layer caching strategy, achieving X MB final image size and reducing build time to under Y minutes"

Metric to measure: docker images output (check SIZE column), docker build time
Realistic starter: 150-250 MB image, 1-2 minute build time

**Bullet 4: Test Coverage**
Template: "Developed comprehensive test suite with pytest achieving X% code coverage and Y test execution time, enabling confident continuous deployment with automated quality gates"

Metric to measure: pytest --cov output, pytest execution time
Realistic starter: 80-90% coverage, under 2 seconds execution

**Bullet 5: DevSecOps Practices**
Template: "Established security-first development workflow with automated SAST scanning and vulnerability assessment, achieving zero high-severity findings while maintaining X-minute average CI pipeline execution time"

Metric to measure: GitHub Actions workflow duration, Semgrep/Trivy results
Realistic starter: 3-5 minute pipeline, 0 HIGH findings (after you fix them)

**Alternative Bullet: API Design**
Template: "Architected RESTful API using FastAPI with Pydantic validation, serving X endpoints with built-in OpenAPI documentation and structured JSON logging for production observability"

Metric to measure: Number of endpoints, response times (use curl with time or hey tool)
Realistic starter: 3 endpoints, sub-50ms response times locally

**How to Measure These:**

For CI time:
- Check GitHub Actions run duration in Actions tab

For security findings:
- Count issues in GitHub Security tab before you fixed them, OR
- Intentionally introduce test vulns, count findings, then remove

For image size:
- Run: docker images | grep fastapi-devsecops-demo

For test coverage:
- Run: pytest --cov=app tests/ (install pytest-cov first)

For response times:
- Run: curl -w "\nTime: %{time_total}s\n" http://localhost:8000/health

---

## SECTION 10 — NEXT ACTION

**Your Next 3 Actions Today:**

1. **Create the project directory and initialize Git** (5 minutes)
   - Run: mkdir fastapi-devsecops-demo && cd fastapi-devsecops-demo
   - Run: git init
   - Create folder structure: app/, tests/, docs/, .github/workflows/

2. **Set up your Python environment** (5 minutes)
   - Run: python3 -m venv venv
   - Run: source venv/bin/activate
   - Create empty requirements.txt

3. **Create your GitHub repository** (5 minutes)
   - Go to GitHub, create new public repo named "fastapi-devsecops-demo"
   - Don't initialize with README (you'll create locally)
   - Link local repo: git remote add origin [your-repo-url]

After these 3 actions, you'll be ready to start Phase 1 (building the microservice).

---

**🎯 CRITICAL: Follow the Phase Order**

Do NOT jump ahead. This exact sequence prevents 80% of beginner frustration:
- Phase 0: Repo setup
- Phase 1: API running locally ← Get this working FIRST
- Phase 2: Tests passing locally ← Verify tests work BEFORE Docker
- Phase 3: Lint/format working
- Phase 4: Docker working
- ONLY THEN: Phase 5-7 (CI, Semgrep, Trivy)
- Finally: Phase 8 (Docs)

Each phase builds on the previous. Skipping ahead = debugging hell.

---

**If you want, reply START CODING and I'll generate the actual files phase-by-phase.**

I'll wait for your confirmation before generating any code. You can also ask questions about any section of this plan, or tell me to adjust specific parts before you begin.
