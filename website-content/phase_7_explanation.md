# Phase 7: Container Scanning with Trivy

## What is Phase 7 About?

Phase 7 adds **container vulnerability scanning** with Trivy. It checks your Docker image for known security vulnerabilities in:
- Your Python dependencies (FastAPI, Pydantic, etc.)
- The base operating system (Debian/Ubuntu packages)
- Your Dockerfile configuration

---

## Semgrep vs Trivy: What's the Difference?

| Semgrep (Phase 6) | Trivy (Phase 7) |
|-------------------|-----------------|
| Scans your **source code** | Scans your **Docker image** |
| Finds bugs you wrote | Finds vulnerabilities in dependencies |
| "Your code has SQL injection" | "FastAPI v0.100.0 has known vulnerability" |
| Catches coding mistakes | Catches outdated/vulnerable packages |

**You need BOTH:**
- Semgrep: Your code is secure
- Trivy: Your dependencies are secure

---

## The Problem Trivy Solves

### Your Code Can Be Perfect, But Still Vulnerable

Imagine you write perfect, secure code. But you use:
- An old version of FastAPI with a security bug
- A Python library that got hacked
- A base image with unpatched Linux vulnerabilities

**Your app is now vulnerable - even though YOUR code is fine.**

### Real-World Example: Log4j (2021)

```
Company: "Our code is secure, we checked!"
Hacker: "But your logging library (Log4j) has a vulnerability"
Result: Millions of systems compromised
```

The company's code was fine. The **dependency** had the bug.

---

## What is Trivy?

Trivy is an open-source security scanner by Aqua Security. It scans:

1. **Container images** - All packages inside your Docker image
2. **Filesystems** - Dependencies in your project
3. **IaC (Infrastructure as Code)** - Dockerfile, Kubernetes configs

### How Trivy Works

```
Your Docker Image
       │
       ▼
┌──────────────────────────────────────────┐
│  Trivy scans:                            │
│                                          │
│  • OS packages (apt, apk)                │
│  • Python packages (pip)                 │
│  • Checks against vulnerability database │
└──────────────────────────────────────────┘
       │
       ▼
Reports: "Found CVE-2024-1234 in package X"
```

---

## What is a CVE?

**CVE = Common Vulnerabilities and Exposures**

It's a unique ID for each known security vulnerability.

**Example:** `CVE-2021-44228` (Log4j vulnerability)

When a vulnerability is discovered:
1. Security researchers find the bug
2. It gets assigned a CVE ID
3. Added to vulnerability databases
4. Scanners like Trivy can now detect it

---

## Real-World Analogy

Think of Trivy like a **car recall checker**:

| Car Recall | Trivy |
|------------|-------|
| "Your car model has a brake defect" | "Your Python package has a security bug" |
| Checks VIN against recall database | Checks packages against CVE database |
| "Recall: Airbag may not deploy" | "CVE-2024-1234: Remote code execution" |
| Fix: Take car to dealer | Fix: Update the package |

You didn't cause the problem, but you need to fix it.

---

## What We Built

### Two Jobs in the Workflow

**Job 1: Container Image Scan**
- Builds your Docker image
- Scans all packages inside
- Reports vulnerabilities

**Job 2: Dockerfile/Config Scan**
- Scans your Dockerfile
- Checks for misconfigurations
- "You're running as root - that's risky"

---

### The Workflow File: `.github/workflows/trivy.yml`

```yaml
name: Trivy Container Scan

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 6 * * 0'  # Weekly on Sundays
```

**Three triggers:**
1. **Push/PR** - Scan when code changes
2. **Weekly schedule** - Catch newly discovered CVEs

---

### Job 1: Container Image Scan

```yaml
- name: Build Docker image for scanning
  uses: docker/build-push-action@v5
  with:
    push: false    # Don't push, just build locally
    load: true     # Load into Docker for scanning
    tags: fastapi-devsecops-demo:${{ github.sha }}

- name: Run Trivy vulnerability scanner
  uses: aquasecurity/trivy-action@master
  with:
    image-ref: fastapi-devsecops-demo:${{ github.sha }}
    format: 'sarif'
    severity: 'CRITICAL,HIGH,MEDIUM'
    exit-code: '0'
```

| Step | What it does |
|------|--------------|
| Build image | Creates Docker image (but doesn't push it) |
| Trivy scan | Scans all packages in the image |
| Upload results | Shows findings in GitHub Security tab |

---

### Job 2: Dockerfile Scan

```yaml
- name: Run Trivy config scanner
  uses: aquasecurity/trivy-action@master
  with:
    scan-type: 'config'    # Scan configuration files
    severity: 'CRITICAL,HIGH,MEDIUM'
```

This scans your Dockerfile for issues like:
- Running as root user
- Using `latest` tag instead of specific version
- Exposing unnecessary ports
- Missing health checks

---

## Severity Levels

Trivy classifies vulnerabilities by severity:

| Severity | Meaning | Action |
|----------|---------|--------|
| **CRITICAL** | Easily exploitable, severe impact | Fix immediately |
| **HIGH** | Significant risk | Fix soon |
| **MEDIUM** | Moderate risk | Plan to fix |
| **LOW** | Minor risk | Fix when convenient |

Our scan focuses on **CRITICAL, HIGH, MEDIUM** - ignoring LOW to reduce noise.

---

## Example Trivy Output

```
┌─────────────────────────────────────────────────────────────────┐
│                    Trivy Scan Results                           │
├───────────────┬──────────┬──────────────────┬──────────────────┤
│ Package       │ Severity │ Vulnerability    │ Fixed In         │
├───────────────┼──────────┼──────────────────┼──────────────────┤
│ openssl       │ HIGH     │ CVE-2024-1234    │ 3.0.12           │
│ curl          │ MEDIUM   │ CVE-2024-5678    │ 8.5.0            │
│ fastapi       │ HIGH     │ CVE-2024-9999    │ 0.110.0          │
└───────────────┴──────────┴──────────────────┴──────────────────┘

Total: 3 vulnerabilities (0 CRITICAL, 2 HIGH, 1 MEDIUM)
```

**What this tells you:**
- Which package has the problem
- How severe it is
- Which version fixes it

---

## Visual Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                   Code pushed / Weekly schedule                  │
└─────────────────────────────────────────────────────────────────┘
                                │
                ┌───────────────┴───────────────┐
                ▼                               ▼
┌───────────────────────────┐   ┌───────────────────────────┐
│  Job 1: Image Scan        │   │  Job 2: Config Scan       │
│                           │   │                           │
│  1. Build Docker image    │   │  1. Scan Dockerfile       │
│  2. Scan all packages     │   │  2. Check for misconfigs  │
│  3. Check CVE database    │   │  3. Report issues         │
│  4. Report vulnerabilities│   │                           │
└───────────────────────────┘   └───────────────────────────┘
                │                               │
                └───────────────┬───────────────┘
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│              Results uploaded to GitHub Security tab             │
└─────────────────────────────────────────────────────────────────┘
```

---

## Why Weekly Scans?

New CVEs are published daily. Your dependencies might be safe today but vulnerable tomorrow.

**Example timeline:**
- Monday: You deploy with FastAPI 0.100.0 ✅
- Wednesday: CVE-2024-9999 published for FastAPI 0.100.0
- Sunday: Weekly Trivy scan detects the new CVE ⚠️
- Monday: You update FastAPI and redeploy ✅

**Without weekly scans, you'd never know!**

---

## Where to See Results

### GitHub Security Tab

1. Go to repository → **Security** → **Code scanning alerts**
2. Filter by **Tool: trivy**
3. See all container vulnerabilities

### Artifacts

Each scan saves results as downloadable artifacts:
- `trivy-results.sarif`
- `trivy-config-results.sarif`

Useful for audits or detailed analysis.

---

## How to Fix Vulnerabilities

### Step 1: Update Dependencies

**Python packages:**
```bash
pip install --upgrade fastapi
```

Then update `requirements.txt` with new version.

### Step 2: Update Base Image

If vulnerability is in OS packages, update Dockerfile:
```dockerfile
# Before
FROM python:3.12-slim

# After (forces fresh pull)
FROM python:3.12-slim@sha256:abc123...
```

### Step 3: Rebuild and Scan Again

```bash
docker build -t myapp .
trivy image myapp
```

Verify the vulnerability is gone.

---

## The Complete Security Picture

With Phases 6 and 7 together:

```
┌─────────────────────────────────────────────────────────────────┐
│                      Your Application                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   Your Code ────────► Semgrep (Phase 6)                         │
│   (app/*.py)          "Your code is secure"                     │
│                                                                  │
│   Dependencies ─────► Trivy (Phase 7)                           │
│   (FastAPI, etc)      "Your packages are secure"                │
│                                                                  │
│   Docker Image ─────► Trivy (Phase 7)                           │
│   (OS packages)       "Your container is secure"                │
│                                                                  │
│   Dockerfile ───────► Trivy (Phase 7)                           │
│   (configuration)     "Your config is secure"                   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**All layers protected!**

---

## Common Mistakes to Avoid

### Mistake 1: Only scanning your code
**Problem:** Dependencies have vulnerabilities
**Fix:** Scan container images with Trivy

### Mistake 2: Never updating base images
**Problem:** Old OS packages accumulate CVEs
**Fix:** Regularly rebuild with latest base image

### Mistake 3: Ignoring all vulnerabilities
**Problem:** "Too many alerts, I'll ignore them"
**Fix:** Focus on CRITICAL/HIGH first

### Mistake 4: No scheduled scans
**Problem:** Miss newly discovered CVEs
**Fix:** Run weekly scans even if code doesn't change

---

## Production-Ready Checklist (Phase 7)

✅ **Trivy workflow created** - `.github/workflows/trivy.yml`
✅ **Container image scanning** - All packages checked
✅ **Dockerfile scanning** - Configuration validated
✅ **Multiple triggers** - Push, PR, and weekly schedule
✅ **Severity filtering** - Focus on CRITICAL/HIGH/MEDIUM
✅ **GitHub Security integration** - Results in Security tab
✅ **Artifact storage** - Results saved for 30 days

---

## Key Takeaway

**Phase 7 protects against supply chain vulnerabilities.**

Your code can be perfect, but if your dependencies are vulnerable, you're vulnerable. Trivy continuously monitors your entire container - OS, packages, and configuration.

This completes the **DevSecOps** approach:
- **Dev:** Build the app (Phases 1-4)
- **Sec:** Scan code and containers (Phases 6-7)
- **Ops:** Automate everything (Phase 5)

---

## Next Steps

Phase 8 finalizes the project with **documentation polish and cleanup** - making everything professional and recruiter-ready.
