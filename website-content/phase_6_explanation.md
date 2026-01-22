# Phase 6: SAST Security Scanning with Semgrep

## What is Phase 6 About?

Phase 6 adds **security scanning** to your CI/CD pipeline. It automatically checks your code for security vulnerabilities before they reach production.

**The goal:** Catch security bugs as early as possible - when they're cheapest to fix.

---

## What is SAST?

**SAST = Static Application Security Testing**

"Static" means it analyzes your **source code** without running the application.

Think of it like a spell checker, but for security:
- Spell checker finds typos in text
- SAST finds security flaws in code

---

## Why Security Scanning Matters

### The Cost of Security Bugs

| When Found | Cost to Fix |
|------------|-------------|
| During coding | $100 |
| During code review | $1,000 |
| During testing | $10,000 |
| In production | $100,000+ |

**Finding security bugs early saves money and reputation.**

### Real-World Disasters

- **Equifax breach (2017):** 147 million people's data exposed. Cost: $1.4 billion. Cause: Known vulnerability not patched.
- **Log4j (2021):** Millions of systems vulnerable. Companies scrambled for weeks to patch.

**These could have been caught with automated security scanning.**

---

## What is Semgrep?

Semgrep is a fast, open-source security scanner that:
- Scans code for security vulnerabilities
- Finds bugs and anti-patterns
- Supports many languages (Python, JavaScript, Go, etc.)
- Has thousands of pre-built rules

### How Semgrep Works

```
Your Code → Semgrep → Matches patterns → Reports vulnerabilities
```

Semgrep has rules like:
- "If you see `eval(user_input)`, flag it as dangerous"
- "If you see SQL built with string concatenation, flag SQL injection risk"
- "If you see hardcoded passwords, flag it"

---

## Real-World Analogy

Think of Semgrep like a **building inspector**:

| Building Inspector | Semgrep |
|--------------------|---------|
| Checks for code violations | Checks for security vulnerabilities |
| "This wire is exposed - fire hazard" | "This input isn't validated - injection risk" |
| "Exit door blocked - safety issue" | "Password hardcoded - security issue" |
| Catches problems before people move in | Catches problems before code goes live |

---

## What Security Issues Does Semgrep Find?

### 1. SQL Injection

**Vulnerable code:**
```python
query = "SELECT * FROM users WHERE name = '" + user_input + "'"
```

**The attack:** User enters `'; DROP TABLE users; --`

**Result:** Your entire users table is deleted!

**Semgrep says:** "Possible SQL injection. Use parameterized queries."

---

### 2. Command Injection

**Vulnerable code:**
```python
import os
os.system("ping " + user_input)
```

**The attack:** User enters `google.com; rm -rf /`

**Result:** Your server files get deleted!

**Semgrep says:** "Possible command injection. Don't pass user input to system commands."

---

### 3. Hardcoded Secrets

**Vulnerable code:**
```python
API_KEY = "sk-12345-secret-key-here"
password = "admin123"
```

**The problem:** Anyone who sees your code (GitHub) now has your credentials.

**Semgrep says:** "Hardcoded secret detected. Use environment variables."

---

### 4. Insecure Deserialization

**Vulnerable code:**
```python
import pickle
data = pickle.loads(user_input)  # DANGEROUS!
```

**The attack:** Attacker sends malicious serialized object that executes code.

**Semgrep says:** "Pickle deserialization of untrusted data is dangerous."

---

### 5. Path Traversal

**Vulnerable code:**
```python
filename = request.args.get('file')
content = open('/uploads/' + filename).read()
```

**The attack:** User enters `../../../etc/passwd`

**Result:** Attacker reads sensitive system files!

**Semgrep says:** "Possible path traversal. Validate file paths."

---

## The OWASP Top 10

Semgrep checks for the **OWASP Top 10** - the most critical web security risks:

1. **Injection** (SQL, Command, etc.)
2. **Broken Authentication**
3. **Sensitive Data Exposure**
4. **XML External Entities (XXE)**
5. **Broken Access Control**
6. **Security Misconfiguration**
7. **Cross-Site Scripting (XSS)**
8. **Insecure Deserialization**
9. **Using Components with Known Vulnerabilities**
10. **Insufficient Logging & Monitoring**

**Our Semgrep setup scans for all of these automatically.**

---

## What We Built

### The Workflow File: `.github/workflows/semgrep.yml`

```yaml
name: Semgrep Security Scan

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 6 * * *'  # Run daily at 6 AM UTC
```

**Three triggers:**
1. **Push to main** - Scan when code is merged
2. **Pull requests** - Scan before code is merged
3. **Scheduled (daily)** - Catch newly discovered vulnerabilities

---

### Why Daily Scans?

New vulnerabilities are discovered constantly. Code that was "safe" yesterday might be "vulnerable" today because:
- New attack techniques discovered
- New Semgrep rules added
- Dependencies found to have issues

**Daily scans catch these even if your code hasn't changed.**

---

### The Workflow Steps

```yaml
steps:
  - name: Checkout code
    uses: actions/checkout@v4

  - name: Setup Python
    uses: actions/setup-python@v5

  - name: Install Semgrep
    run: pip install semgrep

  - name: Run Semgrep scan
    run: semgrep scan --config auto --sarif --output semgrep.sarif || true

  - name: Upload results to GitHub Security tab
    uses: github/codeql-action/upload-sarif@v3
```

| Step | What it does |
|------|--------------|
| Checkout | Get your code |
| Setup Python | Semgrep needs Python |
| Install Semgrep | Download the scanner |
| Run scan | Scan code with auto-detected rules |
| Upload results | Show findings in GitHub Security tab |

---

### Understanding the Scan Command

```bash
semgrep scan --config auto --sarif --output semgrep.sarif || true
```

| Flag | Meaning |
|------|---------|
| `--config auto` | Automatically detect language and use appropriate rules |
| `--sarif` | Output in SARIF format (standard security format) |
| `--output semgrep.sarif` | Save results to file |
| `|| true` | Don't fail the build if vulnerabilities found (non-blocking) |

---

## SARIF Format

**SARIF = Static Analysis Results Interchange Format**

It's a standard format for security tool results. GitHub understands SARIF and can:
- Display results in the Security tab
- Show alerts on specific lines of code
- Track which issues are fixed

---

## Where to See Results

### GitHub Security Tab

1. Go to your repository
2. Click **"Security"** tab
3. Click **"Code scanning alerts"**
4. See all Semgrep findings

Each finding shows:
- What the vulnerability is
- Which file and line
- How to fix it
- Severity level

---

## Visual Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                     Code pushed to GitHub                        │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Semgrep Workflow Triggered                    │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│  Semgrep scans all Python files                                 │
│                                                                  │
│  Checks for:                                                     │
│  • SQL Injection                                                 │
│  • Command Injection                                             │
│  • Hardcoded Secrets                                             │
│  • XSS vulnerabilities                                           │
│  • Insecure configurations                                       │
│  • ... and hundreds more                                         │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│  Results uploaded to GitHub Security tab                         │
│                                                                  │
│  • View all findings                                             │
│  • See affected code lines                                       │
│  • Track fixes over time                                         │
└─────────────────────────────────────────────────────────────────┘
```

---

## Blocking vs Non-Blocking

### Current Setup: Non-Blocking

```yaml
semgrep scan ... || true
```

The `|| true` means: "Even if Semgrep finds issues, don't fail the build."

**Why non-blocking?**
- New projects may have many findings initially
- Allows you to see results without blocking all work
- Can gradually fix issues

### Strict Setup: Blocking

```yaml
semgrep scan --error ...  # Without || true
```

This would fail the build if any vulnerabilities found.

**Use blocking mode when:**
- Project is mature
- Team is ready to fix all issues
- Zero tolerance for new vulnerabilities

---

## Shift-Left Security

This concept is called **"Shift Left"**:

```
Traditional: Code → Test → Deploy → Security Audit (too late!)

Shift Left:  Security → Code → Test → Deploy (catch early!)
```

By adding Semgrep to CI/CD, security moves LEFT in the process - earlier, when it's cheaper to fix.

---

## Common Mistakes to Avoid

### Mistake 1: No security scanning at all
**Problem:** Vulnerabilities discovered in production
**Fix:** Add automated scanning like Semgrep

### Mistake 2: Ignoring all findings
**Problem:** "Too many alerts, I'll ignore them all"
**Fix:** Prioritize by severity, fix critical/high first

### Mistake 3: Only scanning occasionally
**Problem:** Miss newly discovered vulnerabilities
**Fix:** Scan on every push AND daily scheduled scans

### Mistake 4: Not understanding the findings
**Problem:** Can't fix what you don't understand
**Fix:** Read Semgrep's explanations, learn the vulnerability types

---

## Production-Ready Checklist (Phase 6)

✅ **Semgrep workflow created** - `.github/workflows/semgrep.yml`
✅ **Multiple triggers** - Push, PR, and daily schedule
✅ **Auto config** - Detects language and applies appropriate rules
✅ **SARIF output** - Standard security format
✅ **GitHub Security integration** - Results in Security tab
✅ **Non-blocking initially** - See results without breaking builds

---

## Key Takeaway

**Phase 6 automates security.**

Instead of waiting for a security audit (or worse, a breach), Semgrep scans every code change automatically.

This is **DevSecOps** in action - security integrated into the development process, not bolted on at the end.

---

## Next Steps

Phase 7 adds **Trivy container scanning** - checking your Docker images for vulnerabilities in dependencies and the base OS.
