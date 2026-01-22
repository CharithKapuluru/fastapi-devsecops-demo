# Website Design - Batch 1: Foundation Elements

This file contains all the content for the first 5 design elements. Use this to build your website.

---

# Element 1: Interactive Phase Timeline

## Visual Design

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│  [0]────[1]────[2]────[3]────[4]────[5]────[6]────[7]────[8]               │
│   ●──────●──────●──────●──────●──────●──────●──────●──────●                │
│                                                                             │
│  Setup  API   Tests  Lint  Docker CI/CD  SAST  Trivy  Docs                │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Phase Labels (for hover/click)

| Phase | Short Label | Full Title |
|-------|-------------|------------|
| 0 | Setup | Project Setup & Git |
| 1 | API | Build FastAPI Microservice |
| 2 | Tests | Automated Testing with Pytest |
| 3 | Lint | Code Quality with Ruff |
| 4 | Docker | Containerization |
| 5 | CI/CD | GitHub Actions Pipeline |
| 6 | SAST | Security Scanning (Semgrep) |
| 7 | Trivy | Container Scanning |
| 8 | Docs | Documentation & Polish |

## Behavior
- Completed phases: Green color, checkmark icon
- Current phase: Highlighted/pulsing
- Future phases: Grayed out
- Click any phase to jump to it

---

# Element 2: Flashcards for Key Concepts

## How to Use
Each flashcard has a FRONT (question/term) and BACK (answer/explanation).
User clicks to flip.

---

## General Concepts Flashcards

### Card 1: DevOps
**FRONT:**
```
What is DevOps?
```
**BACK:**
```
DevOps = Development + Operations

It's a practice where developers and IT operations
work together to build, test, and release software
faster and more reliably.

Think of it like a relay race - instead of throwing
the baton over a wall, the team passes it smoothly.
```

---

### Card 2: DevSecOps
**FRONT:**
```
What is DevSecOps?
```
**BACK:**
```
DevSecOps = DevOps + Security

Security is built into every step, not added at the end.

Old way: Build → Test → Deploy → Security audit
New way: Security → Build → Security → Test → Security → Deploy

Security becomes everyone's job, not just the security team's.
```

---

### Card 3: REST API
**FRONT:**
```
What is a REST API?
```
**BACK:**
```
A way for applications to talk to each other over the internet.

Like a waiter in a restaurant:
• You (client) tell the waiter what you want
• Waiter goes to kitchen (server)
• Kitchen prepares food (processes request)
• Waiter brings it back (response)

Every app you use (Instagram, Uber, Netflix) uses REST APIs.
```

---

### Card 4: HTTP Methods
**FRONT:**
```
What are HTTP Methods?
(GET, POST, PUT, DELETE)
```
**BACK:**
```
Actions you can perform on data:

GET    → Read data (view a post)
POST   → Create data (write a new post)
PUT    → Update data (edit a post)
DELETE → Remove data (delete a post)

Like a library:
GET = borrow book, POST = donate book,
PUT = replace book, DELETE = remove book
```

---

### Card 5: API Endpoint
**FRONT:**
```
What is an API Endpoint?
```
**BACK:**
```
A specific URL where your app listens for requests.

Like doors in a building:
• /health  → Check if app is alive
• /items   → Get or create items
• /users   → Get or create users

Each door (endpoint) does one specific job.
```

---

### Card 6: FastAPI
**FRONT:**
```
What is FastAPI?
```
**BACK:**
```
A modern Python framework for building APIs.

Why it's better than Flask:
• Faster performance
• Automatic documentation
• Built-in data validation
• Type checking

Used by Microsoft, Uber, Netflix, NASA.
```

---

### Card 7: Pydantic
**FRONT:**
```
What is Pydantic?
```
**BACK:**
```
A Python library for data validation.

Like a form with rules:
• Name: required, max 100 characters
• Email: must be valid format
• Age: must be a number

If data doesn't match rules, it's rejected automatically.
No manual checking needed.
```

---

### Card 8: Docker Image vs Container
**FRONT:**
```
What's the difference between
Docker Image and Container?
```
**BACK:**
```
Image = Recipe/Blueprint (like a cake recipe)
Container = Running instance (like an actual cake)

You create an image once.
You can run many containers from it.

Dockerfile → builds → Image → runs → Container
```

---

### Card 9: Docker
**FRONT:**
```
What is Docker?
```
**BACK:**
```
A tool that packages your app + everything it needs
into a "container" that runs the same everywhere.

Solves: "Works on my machine!" problem

Like a shipping container:
Same box works on any ship, truck, or train.
Same Docker container runs on any computer.
```

---

### Card 10: Dockerfile
**FRONT:**
```
What is a Dockerfile?
```
**BACK:**
```
A recipe that tells Docker how to build your image.

Step by step instructions:
1. Start with Python
2. Copy my code
3. Install dependencies
4. Run the app

Like IKEA furniture instructions - follow steps, get same result every time.
```

---

### Card 11: CI/CD
**FRONT:**
```
What is CI/CD?
```
**BACK:**
```
CI = Continuous Integration
"Automatically test every code change"

CD = Continuous Delivery
"Automatically prepare code for deployment"

Instead of manually testing and deploying:
Push code → Tests run automatically → Build automatically → Ready to deploy
```

---

### Card 12: GitHub Actions
**FRONT:**
```
What is GitHub Actions?
```
**BACK:**
```
GitHub's built-in automation tool.

When you push code, it automatically:
• Runs your tests
• Checks code quality
• Builds Docker images
• Deploys your app

Like a robot assistant that does repetitive tasks for you.
```

---

### Card 13: YAML
**FRONT:**
```
What is YAML?
```
**BACK:**
```
A simple file format for configuration.

Like a structured to-do list:

name: CI Pipeline
steps:
  - run tests
  - build docker
  - deploy

Used for GitHub Actions, Docker Compose, Kubernetes.
Easy to read, easy to write.
```

---

### Card 14: SAST
**FRONT:**
```
What is SAST?
```
**BACK:**
```
SAST = Static Application Security Testing

Scans your SOURCE CODE for security vulnerabilities
without running the app.

Like spell-check, but for security:
• Finds SQL injection risks
• Finds hardcoded passwords
• Finds insecure patterns

Catches bugs before they become breaches.
```

---

### Card 15: Semgrep
**FRONT:**
```
What is Semgrep?
```
**BACK:**
```
A fast, open-source security scanner.

Scans your code and says:
"Hey, line 45 has a potential SQL injection!"

Like a building inspector checking for code violations
before anyone moves in.
```

---

### Card 16: CVE
**FRONT:**
```
What is a CVE?
```
**BACK:**
```
CVE = Common Vulnerabilities and Exposures

A unique ID for each known security bug.

Example: CVE-2021-44228 (Log4j vulnerability)

When a bug is discovered:
1. Gets assigned a CVE ID
2. Added to databases
3. Scanners can now detect it
```

---

### Card 17: Trivy
**FRONT:**
```
What is Trivy?
```
**BACK:**
```
A container security scanner.

Scans your Docker image for:
• Vulnerable OS packages
• Vulnerable Python libraries
• Dockerfile misconfigurations

Your code can be perfect, but if your dependencies
have bugs, you're still vulnerable.
```

---

### Card 18: Pytest
**FRONT:**
```
What is Pytest?
```
**BACK:**
```
Python's most popular testing framework.

Write tests like:

def test_addition():
    assert 1 + 1 == 2

If true → test passes ✓
If false → test fails ✗

Run all tests with one command: pytest
```

---

### Card 19: Linting
**FRONT:**
```
What is Linting?
```
**BACK:**
```
Automatically checking code for problems.

Like spell-check + grammar-check for code:
• Unused variables
• Missing imports
• Bad formatting
• Common bugs

Catches mistakes before you run the code.
```

---

### Card 20: SARIF
**FRONT:**
```
What is SARIF?
```
**BACK:**
```
SARIF = Static Analysis Results Interchange Format

A standard format for security scan results.

Like PDF for documents - any tool can read it.

GitHub understands SARIF and shows results
in the Security tab automatically.
```

---

# Element 3: Key Takeaway Boxes

Use these at the end of each phase.

---

## Phase 0: Setup
```
┌─────────────────────────────────────────────────────────────┐
│  💡 Key Takeaway                                            │
│                                                             │
│  A well-organized project structure and Git setup is the   │
│  foundation everything else builds on. Skip this, and      │
│  you'll struggle later.                                    │
└─────────────────────────────────────────────────────────────┘
```

---

## Phase 1: FastAPI
```
┌─────────────────────────────────────────────────────────────┐
│  💡 Key Takeaway                                            │
│                                                             │
│  Production APIs need validation, logging, and error       │
│  handling from day one. A "Hello World" API won't          │
│  impress anyone.                                           │
└─────────────────────────────────────────────────────────────┘
```

---

## Phase 2: Testing
```
┌─────────────────────────────────────────────────────────────┐
│  💡 Key Takeaway                                            │
│                                                             │
│  Tests PROVE your code works. Anyone can say "it works"    │
│  - tests provide evidence. No tests = no job offer.        │
└─────────────────────────────────────────────────────────────┘
```

---

## Phase 3: Linting
```
┌─────────────────────────────────────────────────────────────┐
│  💡 Key Takeaway                                            │
│                                                             │
│  Linting catches bugs before you run the code. It's like   │
│  spell-check for programming. Every professional team      │
│  uses it.                                                  │
└─────────────────────────────────────────────────────────────┘
```

---

## Phase 4: Docker
```
┌─────────────────────────────────────────────────────────────┐
│  💡 Key Takeaway                                            │
│                                                             │
│  Docker makes "works on my machine" become "works on       │
│  EVERY machine." This is how all modern apps are deployed. │
└─────────────────────────────────────────────────────────────┘
```

---

## Phase 5: CI/CD
```
┌─────────────────────────────────────────────────────────────┐
│  💡 Key Takeaway                                            │
│                                                             │
│  CI/CD automates quality control. Every push is tested,    │
│  checked, and built automatically. No exceptions, no       │
│  shortcuts.                                                │
└─────────────────────────────────────────────────────────────┘
```

---

## Phase 6: Semgrep
```
┌─────────────────────────────────────────────────────────────┐
│  💡 Key Takeaway                                            │
│                                                             │
│  Security scanning catches vulnerabilities before hackers  │
│  do. Finding bugs in development costs $100. Finding them  │
│  in production costs $100,000+.                            │
└─────────────────────────────────────────────────────────────┘
```

---

## Phase 7: Trivy
```
┌─────────────────────────────────────────────────────────────┐
│  💡 Key Takeaway                                            │
│                                                             │
│  Your code can be perfect, but vulnerable dependencies     │
│  make you vulnerable. Trivy scans everything inside your   │
│  container.                                                │
└─────────────────────────────────────────────────────────────┘
```

---

## Phase 8: Documentation
```
┌─────────────────────────────────────────────────────────────┐
│  💡 Key Takeaway                                            │
│                                                             │
│  Recruiters spend 30 seconds on your GitHub. Professional  │
│  documentation is the difference between "some project"    │
│  and "let's interview this person."                        │
└─────────────────────────────────────────────────────────────┘
```

---

# Element 4: Before vs After Comparisons

## Main Comparison (Homepage)

```
┌────────────────────────────────┬────────────────────────────────┐
│      BASIC STUDENT PROJECT     │     PRODUCTION-READY PROJECT   │
├────────────────────────────────┼────────────────────────────────┤
│                                │                                │
│  ❌ No tests                   │  ✅ 18+ automated tests        │
│                                │                                │
│  ❌ No CI/CD                   │  ✅ GitHub Actions pipeline    │
│                                │                                │
│  ❌ No security scanning       │  ✅ Semgrep + Trivy            │
│                                │                                │
│  ❌ print() for debugging      │  ✅ Structured JSON logging    │
│                                │                                │
│  ❌ "Works on my machine"      │  ✅ Docker runs everywhere     │
│                                │                                │
│  ❌ No documentation           │  ✅ Professional README        │
│                                │                                │
│  ❌ No code quality checks     │  ✅ Ruff linting & formatting  │
│                                │                                │
│  ❌ Manual everything          │  ✅ Automated everything       │
│                                │                                │
├────────────────────────────────┼────────────────────────────────┤
│       Gets ignored             │       Gets interviews          │
└────────────────────────────────┴────────────────────────────────┘
```

---

## Phase 1: API Comparison

```
┌────────────────────────────────┬────────────────────────────────┐
│         BASIC API              │      PRODUCTION API            │
├────────────────────────────────┼────────────────────────────────┤
│                                │                                │
│  @app.route('/hello')          │  @app.get("/items",            │
│  def hello():                  │      response_model=list[Item])│
│      return "Hello"            │  async def get_items():        │
│                                │      logger.info("Request")    │
│                                │      return items              │
│                                │                                │
│  No validation                 │  Pydantic validation           │
│  No logging                    │  JSON structured logging       │
│  No error handling             │  Try/except + global handler   │
│  No documentation              │  Auto-generated docs           │
│                                │                                │
└────────────────────────────────┴────────────────────────────────┘
```

---

## Phase 2: Testing Comparison

```
┌────────────────────────────────┬────────────────────────────────┐
│       WITHOUT TESTS            │        WITH TESTS              │
├────────────────────────────────┼────────────────────────────────┤
│                                │                                │
│  "I tested it manually"        │  pytest tests/ -v              │
│  "It worked yesterday"         │  18 passed in 0.33s ✓          │
│  "Trust me, it's fine"         │  100% reproducible             │
│                                │                                │
│  Change code → Maybe breaks    │  Change code → Tests catch it  │
│  Find bugs in production       │  Find bugs immediately         │
│  Users report issues           │  CI reports issues             │
│                                │                                │
└────────────────────────────────┴────────────────────────────────┘
```

---

## Phase 4: Docker Comparison

```
┌────────────────────────────────┬────────────────────────────────┐
│       WITHOUT DOCKER           │        WITH DOCKER             │
├────────────────────────────────┼────────────────────────────────┤
│                                │                                │
│  "Works on my machine!"        │  Works on EVERY machine        │
│                                │                                │
│  Dev: Python 3.12              │  Same Python everywhere        │
│  Server: Python 3.9 💥         │                                │
│                                │                                │
│  "Install these 20 things..."  │  docker run myapp              │
│                                │                                │
│  Different OS = Different bugs │  Same container = Same result  │
│                                │                                │
└────────────────────────────────┴────────────────────────────────┘
```

---

## Phase 5: CI/CD Comparison

```
┌────────────────────────────────┬────────────────────────────────┐
│       MANUAL PROCESS           │        WITH CI/CD              │
├────────────────────────────────┼────────────────────────────────┤
│                                │                                │
│  1. Write code                 │  1. Write code                 │
│  2. Maybe run tests            │  2. Push to GitHub             │
│  3. Maybe check linting        │  3. ☕ Get coffee              │
│  4. Manually build Docker      │  4. Everything runs auto       │
│  5. Manually push image        │                                │
│  6. Hope nothing broke         │  Tests ✓ Lint ✓ Build ✓        │
│                                │                                │
│  Takes: 30 minutes             │  Takes: 2 minutes              │
│  Reliability: 😬               │  Reliability: 💯               │
│                                │                                │
└────────────────────────────────┴────────────────────────────────┘
```

---

# Element 5: Difficulty & Time Indicators

Place these at the top of each phase page.

---

## Phase 0: Setup
```
┌─────────────────────────────────────────────────────────────┐
│  Phase 0: Project Setup & Git                               │
│                                                             │
│  ⏱️ Reading time: 5 mins                                    │
│  📊 Difficulty: Beginner                                    │
│  🔧 Hands-on: Yes (terminal commands)                       │
│  📋 Prerequisites: None                                     │
└─────────────────────────────────────────────────────────────┘
```

---

## Phase 1: FastAPI
```
┌─────────────────────────────────────────────────────────────┐
│  Phase 1: Build FastAPI Microservice                        │
│                                                             │
│  ⏱️ Reading time: 15 mins                                   │
│  📊 Difficulty: Beginner-Intermediate                       │
│  🔧 Hands-on: Yes (Python code)                             │
│  📋 Prerequisites: Basic Python knowledge                   │
└─────────────────────────────────────────────────────────────┘
```

---

## Phase 2: Testing
```
┌─────────────────────────────────────────────────────────────┐
│  Phase 2: Automated Testing with Pytest                     │
│                                                             │
│  ⏱️ Reading time: 12 mins                                   │
│  📊 Difficulty: Beginner-Intermediate                       │
│  🔧 Hands-on: Yes (writing tests)                           │
│  📋 Prerequisites: Phase 1 completed                        │
└─────────────────────────────────────────────────────────────┘
```

---

## Phase 3: Linting
```
┌─────────────────────────────────────────────────────────────┐
│  Phase 3: Code Quality with Ruff                            │
│                                                             │
│  ⏱️ Reading time: 8 mins                                    │
│  📊 Difficulty: Beginner                                    │
│  🔧 Hands-on: Yes (configuration)                           │
│  📋 Prerequisites: Phase 1 completed                        │
└─────────────────────────────────────────────────────────────┘
```

---

## Phase 4: Docker
```
┌─────────────────────────────────────────────────────────────┐
│  Phase 4: Docker Containerization                           │
│                                                             │
│  ⏱️ Reading time: 12 mins                                   │
│  📊 Difficulty: Intermediate                                │
│  🔧 Hands-on: Yes (Docker commands)                         │
│  📋 Prerequisites: Docker installed                         │
└─────────────────────────────────────────────────────────────┘
```

---

## Phase 5: CI/CD
```
┌─────────────────────────────────────────────────────────────┐
│  Phase 5: CI/CD with GitHub Actions                         │
│                                                             │
│  ⏱️ Reading time: 12 mins                                   │
│  📊 Difficulty: Intermediate                                │
│  🔧 Hands-on: Yes (YAML configuration)                      │
│  📋 Prerequisites: GitHub account                           │
└─────────────────────────────────────────────────────────────┘
```

---

## Phase 6: Semgrep
```
┌─────────────────────────────────────────────────────────────┐
│  Phase 6: Security Scanning with Semgrep                    │
│                                                             │
│  ⏱️ Reading time: 10 mins                                   │
│  📊 Difficulty: Intermediate                                │
│  🔧 Hands-on: Yes (workflow setup)                          │
│  📋 Prerequisites: Phase 5 completed                        │
└─────────────────────────────────────────────────────────────┘
```

---

## Phase 7: Trivy
```
┌─────────────────────────────────────────────────────────────┐
│  Phase 7: Container Scanning with Trivy                     │
│                                                             │
│  ⏱️ Reading time: 10 mins                                   │
│  📊 Difficulty: Intermediate                                │
│  🔧 Hands-on: Yes (workflow setup)                          │
│  📋 Prerequisites: Phase 4 & 5 completed                    │
└─────────────────────────────────────────────────────────────┘
```

---

## Phase 8: Documentation
```
┌─────────────────────────────────────────────────────────────┐
│  Phase 8: Documentation & Polish                            │
│                                                             │
│  ⏱️ Reading time: 8 mins                                    │
│  📊 Difficulty: Beginner                                    │
│  🔧 Hands-on: Yes (writing docs)                            │
│  📋 Prerequisites: All phases completed                     │
└─────────────────────────────────────────────────────────────┘
```

---

# Summary

## Batch 1 Complete! ✓

You now have content for:

| Element | What You Got |
|---------|--------------|
| 1. Phase Timeline | Labels and behavior for all 9 phases |
| 2. Flashcards | 20 flashcards covering all key concepts |
| 3. Key Takeaways | 9 takeaway boxes (one per phase) |
| 4. Before/After | 5 comparison tables |
| 5. Difficulty Indicators | 9 info boxes (one per phase) |

---

Ready for Batch 2 when you are!
