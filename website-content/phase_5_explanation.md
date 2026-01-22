# Phase 5: CI/CD with GitHub Actions

## What is Phase 5 About?

Phase 5 sets up **CI/CD** - a system that automatically tests, checks, and builds your code every time you push to GitHub.

**No more manual checking.** Push code → GitHub does everything automatically.

---

## What is CI/CD?

### CI = Continuous Integration

**"Continuously check that new code doesn't break anything"**

Every time you push code:
1. Run all tests
2. Check code style (linting)
3. Report if anything fails

### CD = Continuous Delivery/Deployment

**"Continuously prepare code to be deployed"**

After tests pass:
1. Build Docker image
2. Push to container registry
3. Ready to deploy anytime

---

## The Problem CI/CD Solves

### Without CI/CD (Manual Process)

```
Developer writes code
    ↓
Developer runs tests locally (maybe forgets)
    ↓
Developer pushes to GitHub
    ↓
Code reviewer checks manually
    ↓
Someone manually builds Docker image
    ↓
Someone manually deploys
    ↓
Bug found in production 😱
```

**Problems:**
- Easy to forget running tests
- Different developers have different environments
- Manual steps = human errors
- Bugs reach production

### With CI/CD (Automated)

```
Developer pushes code
    ↓
GitHub Actions automatically:
  ✓ Runs linting
  ✓ Runs all tests
  ✓ Builds Docker image
  ✓ Pushes to registry
    ↓
If anything fails → Developer notified immediately
If everything passes → Ready to deploy
```

**Benefits:**
- Nothing gets skipped
- Same checks every time
- Bugs caught before merging
- Fast feedback

---

## Real-World Analogy

Think of CI/CD like an **airport security checkpoint**:

| Airport | CI/CD |
|---------|-------|
| Every passenger goes through security | Every code push goes through checks |
| X-ray scans bags | Linting scans code |
| Metal detector | Tests verify functionality |
| No exceptions | Automated, consistent |
| Catch problems before boarding | Catch bugs before deployment |

You wouldn't let passengers skip security. Same with code - every change must pass checks.

---

## What is GitHub Actions?

GitHub Actions is GitHub's built-in CI/CD system. It:
- Runs automatically when you push code
- Uses YAML files to define what to do
- Provides free compute for public repos
- Shows results directly in GitHub

---

## What We Built

### The Workflow File: `.github/workflows/ci.yml`

This file tells GitHub Actions what to do when code is pushed.

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
```

**This means:** Run this workflow when:
- Someone pushes to `main` branch
- Someone opens a pull request to `main`

---

## The Two Jobs We Created

### Job 1: Lint and Test

```yaml
jobs:
  lint-and-test:
    name: Lint and Test
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python 3.12
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Run Ruff linting
        run: ruff check app/ tests/

      - name: Run Ruff formatting check
        run: ruff format --check app/ tests/

      - name: Run tests with pytest
        run: pytest tests/ -v
```

**What each step does:**

| Step | Purpose |
|------|---------|
| Checkout code | Download your code to the runner |
| Set up Python | Install Python 3.12 |
| Install dependencies | Install FastAPI, pytest, etc. |
| Run Ruff linting | Check for code problems |
| Run Ruff formatting | Verify code is formatted |
| Run tests | Execute all pytest tests |

**If ANY step fails → Whole job fails → You get notified**

---

### Job 2: Build and Push Docker Image

```yaml
build-and-push:
  name: Build and Push Docker Image
  runs-on: ubuntu-latest
  needs: lint-and-test
  if: github.event_name == 'push' && github.ref == 'refs/heads/main'
```

**Key points:**
- `needs: lint-and-test` → Only runs if Job 1 passes
- `if: ...push...main` → Only runs on pushes to main (not PRs)

**Steps:**
1. Build Docker image
2. Log in to GitHub Container Registry
3. Push image with tags (latest, branch name, commit SHA)

---

## Visual Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                     You push code to GitHub                      │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    GitHub Actions Triggered                      │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│  Job 1: Lint and Test                                           │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐            │
│  │ Checkout│→ │ Setup   │→ │ Install │→ │  Lint   │→           │
│  │  Code   │  │ Python  │  │  Deps   │  │ (Ruff)  │            │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘            │
│                                              │                   │
│                                              ▼                   │
│                                         ┌─────────┐             │
│                                         │  Test   │             │
│                                         │(pytest) │             │
│                                         └─────────┘             │
└─────────────────────────────────────────────────────────────────┘
                                │
                         (if passed)
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│  Job 2: Build and Push (only on main branch)                    │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐                         │
│  │  Build  │→ │ Login   │→ │  Push   │                         │
│  │  Image  │  │  GHCR   │  │  Image  │                         │
│  └─────────┘  └─────────┘  └─────────┘                         │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│              ✅ Success! Image ready at ghcr.io                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Understanding the Workflow File

### Triggers (`on:`)

```yaml
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
```

| Event | When it happens |
|-------|-----------------|
| `push` to main | Code merged/pushed directly to main |
| `pull_request` to main | Someone opens a PR targeting main |

### Permissions

```yaml
permissions:
  contents: read        # Read code
  security-events: write # For security scanning (later phases)
  packages: write       # Push Docker images
```

### Runner

```yaml
runs-on: ubuntu-latest
```

GitHub provides a fresh Ubuntu virtual machine to run your jobs. It's free for public repos.

### Dependencies Between Jobs

```yaml
build-and-push:
  needs: lint-and-test
```

Job 2 won't start until Job 1 passes. This ensures we don't build broken code.

---

## Docker Image Tags

When we push the Docker image, it gets multiple tags:

```yaml
tags: |
  type=ref,event=branch       # "main"
  type=sha,prefix={{branch}}- # "main-abc1234"
  type=raw,value=latest       # "latest"
```

**Result:**
```
ghcr.io/yourname/repo:latest
ghcr.io/yourname/repo:main
ghcr.io/yourname/repo:main-abc1234
```

**Why multiple tags?**
- `latest` → Always points to newest version
- `main` → Current main branch
- `main-abc1234` → Specific commit (for rollback)

---

## Where to See Results

### In GitHub

1. Go to your repository
2. Click **"Actions"** tab
3. See all workflow runs
4. Green ✓ = passed, Red ✗ = failed

### On Pull Requests

When you open a PR:
- GitHub shows check status
- Can't merge if checks fail (if branch protection enabled)
- Reviewers see test results

---

## What Happens When Tests Fail?

```
Developer pushes code with bug
    ↓
GitHub Actions runs tests
    ↓
Test fails!
    ↓
Workflow shows ❌
    ↓
Developer gets email notification
    ↓
Developer fixes bug and pushes again
    ↓
Tests pass ✅
    ↓
Safe to merge
```

**Bugs caught BEFORE they reach production!**

---

## GitHub Container Registry (GHCR)

Our workflow pushes Docker images to `ghcr.io` (GitHub Container Registry).

**Benefits:**
- Free for public repos
- Integrated with GitHub (same account)
- Images stored alongside your code
- Easy access control

**Image URL format:**
```
ghcr.io/username/repository:tag
ghcr.io/charith/fastapi-devsecops-demo:latest
```

---

## Common CI/CD Patterns

### Pattern 1: Gate on Main Branch

Only merge to main if all checks pass. This keeps main branch always working.

### Pattern 2: Build Only on Main

PRs run tests, but Docker build only happens when merged to main. Saves resources.

### Pattern 3: Use Caching

```yaml
cache: "pip"
```

Cache dependencies between runs. Second run is much faster.

---

## Common Mistakes to Avoid

### Mistake 1: No CI/CD at all
**Problem:** Bugs slip through
**Fix:** Always have automated checks

### Mistake 2: Skipping checks for "quick fixes"
**Problem:** Quick fixes often break things
**Fix:** Every change goes through CI/CD, no exceptions

### Mistake 3: Not failing fast
**Problem:** Waiting 10 minutes to find out first step failed
**Fix:** Order steps from fastest to slowest (lint before build)

### Mistake 4: Ignoring flaky tests
**Problem:** Tests sometimes pass, sometimes fail
**Fix:** Fix or remove flaky tests - they erode trust in CI

### Mistake 5: Not caching dependencies
**Problem:** Every run installs everything from scratch
**Fix:** Use caching for faster builds

---

## Production-Ready Checklist (Phase 5)

✅ **Workflow file created** - `.github/workflows/ci.yml`
✅ **Triggers configured** - Push and PR to main
✅ **Linting in CI** - Ruff checks run automatically
✅ **Tests in CI** - Pytest runs automatically
✅ **Docker build** - Image built on successful merge
✅ **Container registry** - Images pushed to ghcr.io
✅ **Job dependencies** - Build only after tests pass
✅ **Caching** - Pip cache for faster builds

---

## Key Takeaway

**CI/CD automates quality control.**

Instead of relying on developers to remember to run tests, CI/CD runs them automatically on every push. No exceptions, no shortcuts.

Every professional team uses CI/CD. It's not optional - it's expected.

---

## Next Steps

Phase 6 adds **SAST (Static Application Security Testing)** with Semgrep - scanning code for security vulnerabilities automatically in CI.
