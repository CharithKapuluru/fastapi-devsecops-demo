# Phase 3: Add Linting and Code Formatting

## What is Phase 3 About?

Phase 3 adds **automatic code quality checks** to your project. It ensures your code:
- Follows Python best practices
- Has consistent style (indentation, quotes, spacing)
- Doesn't have common bugs or bad patterns

---

## First, Let's Understand the Problem

### The Messy Code Problem

Imagine a team of 5 developers. Each writes code differently:

**Developer 1:**
```python
def get_items( ):
    return {"items":[1,2,3]}
```

**Developer 2:**
```python
def get_items():
    return { "items": [1, 2, 3] }
```

**Developer 3:**
```python
def get_items():
    return {'items': [1, 2, 3]}
```

All three work! But the codebase looks messy and inconsistent.

**Real problems this causes:**
- Hard to read when styles mix
- Code reviews waste time on "add a space here"
- Git diffs show style changes mixed with real changes
- New developers don't know which style to follow

---

## Two Concepts: Linting vs Formatting

### Linting = Finding Problems

A **linter** scans your code and says: "Hey, this might be a bug!" or "This is bad practice!"

**Examples of what linters catch:**

```python
# Unused variable (why define it if you never use it?)
x = 10  # ← Linter: "x is defined but never used"

# Undefined variable (typo?)
print(naem)  # ← Linter: "naem is not defined. Did you mean 'name'?"

# Import not used
import os  # ← Linter: "os imported but never used"

# Comparing to None wrong
if x == None:  # ← Linter: "Use 'x is None' instead"
```

**Linting finds bugs BEFORE you run the code.**

---

### Formatting = Making Code Pretty

A **formatter** automatically fixes your code style to be consistent.

**Before formatting:**
```python
def hello( name ):
    return "Hello, "+name
x=1
y =  2
items = [1,2,3,4]
```

**After formatting:**
```python
def hello(name):
    return "Hello, " + name

x = 1
y = 2
items = [1, 2, 3, 4]
```

**Formatting makes code consistent without changing what it does.**

---

## What is Ruff?

**Ruff** is a modern Python tool that does BOTH linting and formatting. It's:

- **Fast** - Written in Rust, 10-100x faster than older tools
- **All-in-one** - Replaces multiple tools (flake8, isort, black, pyupgrade)
- **Modern** - New standard in Python community

**Before Ruff (needed multiple tools):**
```
flake8    → Linting
black     → Formatting
isort     → Import sorting
pyupgrade → Modernize syntax
```

**With Ruff (one tool does all):**
```
ruff → Everything
```

---

## Real-World Analogy

Think of Ruff like **spell check + grammar check** in Microsoft Word:

| Word Feature | Ruff Equivalent |
|--------------|-----------------|
| Red underline (spelling error) | Linting (finds bugs) |
| Blue underline (grammar issue) | Linting (finds bad practices) |
| Auto-correct | Formatting (fixes style automatically) |

You wouldn't submit a professional document without spell check. Same with code - you don't submit without linting.

---

## What We Configured

We created `pyproject.toml` with Ruff settings:

### Line Length
```toml
line-length = 100
```
No line should exceed 100 characters. Long lines are hard to read.

### Python Version
```toml
target-version = "py312"
```
We're using Python 3.12 features.

### What Rules to Check
```toml
select = [
    "E",   # Style errors (wrong indentation, spacing)
    "W",   # Style warnings
    "F",   # Logic errors (undefined variables, unused imports)
    "I",   # Import sorting (group and alphabetize imports)
    "N",   # Naming conventions (functions lowercase, classes CamelCase)
    "UP",  # Modern Python (use newer syntax)
    "B",   # Common bugs (mutable default arguments, etc.)
    "C4",  # Better list/dict comprehensions
    "SIM", # Simplify code (unnecessary else, etc.)
]
```

### Formatting Style
```toml
quote-style = "double"    # Use "hello" not 'hello'
indent-style = "space"    # Use spaces, not tabs
line-ending = "lf"        # Unix-style line endings
```

---

## How to Use Ruff

### Check for Problems (Linting)
```bash
ruff check app/ tests/
```

**Example output:**
```
app/main.py:15:1: F401 `os` imported but unused
app/main.py:23:5: F841 Local variable `x` is assigned but never used
Found 2 errors.
```

### Fix Problems Automatically
```bash
ruff check app/ tests/ --fix
```
Ruff fixes what it can automatically (like removing unused imports).

### Format Code
```bash
ruff format app/ tests/
```
Automatically reformats all code to be consistent.

---

## What Ruff Catches (Examples)

### Example 1: Unused Import
```python
import os  # You imported this but never used it

def hello():
    return "Hello"
```
**Ruff says:** `F401: 'os' imported but unused`

**Why it matters:** Unused imports slow down your app and confuse readers.

---

### Example 2: Undefined Variable
```python
def greet(name):
    return "Hello, " + naem  # Typo! Should be 'name'
```
**Ruff says:** `F821: Undefined name 'naem'`

**Why it matters:** This would crash at runtime. Ruff catches it before you run.

---

### Example 3: Bad Comparison
```python
if x == None:  # Works but not Pythonic
    print("x is empty")
```
**Ruff says:** `E711: Comparison to None should be 'x is None'`

**Why it matters:** `is None` is faster and more correct in Python.

---

### Example 4: Mutable Default Argument
```python
def add_item(item, items=[]):  # DANGEROUS!
    items.append(item)
    return items
```
**Ruff says:** `B006: Do not use mutable data structures for argument defaults`

**Why it matters:** This is a famous Python bug. The empty list is shared between all calls!

```python
add_item("a")  # Returns ["a"]
add_item("b")  # Returns ["a", "b"] ← Bug! Expected ["b"]
```

---

### Example 5: Unsorted Imports
```python
import os
import sys
from fastapi import FastAPI
import json
from app.config import settings
```
**After Ruff sorts them:**
```python
import json
import os
import sys

from fastapi import FastAPI

from app.config import settings
```
Groups: standard library → third-party → local imports

---

## Why This Matters

### Without Linting/Formatting:
- Bugs hide in code until runtime
- Code reviews argue about style
- Codebase looks messy
- New developers confused about conventions

### With Linting/Formatting:
- Bugs caught before running
- No style debates (Ruff decides)
- Consistent, professional codebase
- Clear conventions for everyone

---

## The Makefile Commands

We added shortcuts:

```makefile
lint:
    ruff check app/ tests/

format:
    ruff format app/ tests/
```

Now just run:
```bash
make lint     # Check for problems
make format   # Fix formatting
```

---

## How This Fits in CI/CD (Phase 5)

Later, GitHub Actions will run `ruff check` automatically on every push:

```
Developer pushes code
    ↓
GitHub runs: ruff check
    ↓
If errors found → Build fails → Developer must fix
If no errors → Build continues
```

This **prevents bad code from ever reaching the main branch**.

---

## Common Mistakes to Avoid

### Mistake 1: Ignoring linting errors
**Problem:** "It works, so I'll ignore the warning"
**Reality:** Those warnings often become bugs later

### Mistake 2: Not running formatter before commit
**Problem:** Code review shows 500 lines changed, but only 5 were real changes
**Fix:** Always run `make format` before committing

### Mistake 3: Each developer using different tools
**Problem:** Developer A uses black, Developer B uses autopep8 → constant reformatting
**Fix:** Team agrees on one tool (Ruff) configured in the project

---

## Production-Ready Checklist (Phase 3)

✅ **Linter configured** - Ruff checks for bugs and bad practices
✅ **Formatter configured** - Consistent code style
✅ **Rules selected** - Appropriate rules for the project
✅ **Makefile commands** - Easy `make lint` and `make format`
✅ **pyproject.toml** - Configuration in standard location
✅ **All code passes** - No linting errors in codebase

---

## Key Takeaway

**Phase 3 automates code quality.**

Instead of relying on humans to catch style issues and common bugs, Ruff does it automatically in seconds.

Professional teams **require** code to pass linting before it can be merged. This isn't optional - it's expected.

---

## Next Steps

Phase 4 adds **Docker containerization** - packaging your app so it runs the same everywhere.
