# Phase 2: Add Automated Tests with Pytest

## What is Phase 2 About?

Phase 2 adds **automated testing** to your API. Instead of manually testing your endpoints by running curl commands, you write code that tests your code automatically.

**Why is this critical?**

Without tests:
```
Make a change → Manually test 5 endpoints → Miss one → Bug in production → Users angry
```

With tests:
```
Make a change → Run `pytest` → All 20 tests pass in 2 seconds → Confident deployment
```

---

## Why Testing Matters

### The Real-World Problem

Imagine you have an API with 10 endpoints. Every time you change code, you need to verify nothing broke.

**Manual testing:**
- Test each endpoint
- Test with valid data
- Test with invalid data
- Test edge cases
- Takes 30+ minutes
- Easy to forget something

**Automated testing:**
- Run one command: `pytest`
- All tests run in seconds
- Never forgets a test case
- Runs the same way every time

### What Companies Expect

Every professional software team requires:
- Tests before merging code
- CI/CD pipelines that run tests automatically
- Code coverage metrics

**No tests = No job offer.** It's that simple.

---

## What is Pytest?

Pytest is Python's most popular testing framework. It's:
- **Simple** - Write tests as regular functions
- **Powerful** - Fixtures, parameterization, plugins
- **Industry standard** - Used by almost every Python project

### Basic Pytest Concept

```python
def test_addition():
    result = 1 + 1
    assert result == 2  # If true, test passes. If false, test fails.
```

The `assert` statement is the heart of testing:
- `assert True` → Test passes
- `assert False` → Test fails

---

## What We Built in Phase 2

We created one file: `tests/test_api.py`

This file contains **20+ tests** organized into 5 test classes:
1. `TestHealthEndpoint` - Tests for `/health`
2. `TestGetItemsEndpoint` - Tests for `GET /items`
3. `TestPostItemsEndpoint` - Tests for `POST /items`
4. `TestItemValidation` - Tests for data validation rules
5. `TestAPIResponseFormat` - Tests for response structure

---

## Key Concept 1: TestClient

FastAPI provides a special testing tool called `TestClient`. It simulates HTTP requests without running a real server.

```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# Now you can make requests:
response = client.get("/health")
response = client.post("/items", json={"name": "Test"})
```

**Why is this important?**

- No need to start a real server
- Tests run fast (milliseconds, not seconds)
- Can test in isolation

---

## Key Concept 2: Fixtures (Test Setup)

**The Problem:**

Each test might create items. If tests share the same database, they interfere with each other:
- Test 1 creates Item ID 1
- Test 2 expects empty database but finds Item ID 1
- Test 2 fails (even though the code is correct!)

**The Solution: Fixtures**

```python
@pytest.fixture(autouse=True)
def reset_items_db():
    """Reset database before each test."""
    items_db.clear()
    next_item_id[0] = 1
    yield  # Test runs here
    items_db.clear()
    next_item_id[0] = 1
```

**What this does:**
1. Before each test: Clear the database, reset ID counter
2. Run the test
3. After each test: Clean up again

**`autouse=True`** means this fixture runs automatically for every test - you don't have to call it.

This ensures **test isolation** - each test starts with a clean slate.

---

## Key Concept 3: Test Organization

We organize tests into classes by what they're testing:

```python
class TestHealthEndpoint:
    """Tests for the health check endpoint."""

    def test_health_check_returns_ok(self):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}
```

**Why classes?**
- Groups related tests together
- Easy to run specific groups: `pytest -k TestHealthEndpoint`
- Clear organization for large test suites

---

## The Tests We Wrote

### Health Endpoint Tests

**What we test:**
- Returns status code 200
- Returns `{"status": "ok"}`
- Returns JSON content type

**Why:** Health checks are critical for production monitoring. If this fails, your load balancer thinks the app is dead.

### GET /items Tests

**What we test:**
- Empty list when no items exist
- Returns items after creation
- Returns multiple items correctly
- IDs are assigned correctly

**Why:** Verifies the read operation works in all scenarios.

### POST /items Tests

**What we test:**
- Creating item with name and description works
- Creating item with only name works (description optional)
- Missing name returns 422 error
- Empty name returns 422 error
- Wrong data type returns 422 error
- IDs auto-increment correctly
- Created items are retrievable

**Why:** The create operation has many edge cases. Tests catch validation issues.

### Validation Tests

**What we test:**
- Name over 100 characters fails
- Description over 500 characters fails
- Name at exactly 100 characters works
- Description at exactly 500 characters works

**Why:** Boundary testing catches off-by-one errors. Does `max_length=100` mean 100 is allowed or rejected?

### Response Format Tests

**What we test:**
- All endpoints return JSON
- Created items have all required fields
- Field types are correct (id is int, name is string)

**Why:** API contracts matter. Frontend developers rely on consistent response formats.

---

## Running Tests

**Run all tests:**
```bash
pytest tests/ -v
```

**Output:**
```
tests/test_api.py::TestHealthEndpoint::test_health_check_returns_ok PASSED
tests/test_api.py::TestHealthEndpoint::test_health_check_returns_json PASSED
tests/test_api.py::TestGetItemsEndpoint::test_get_items_empty_list PASSED
... (20+ tests)

========================= 20 passed in 0.45s =========================
```

**The `-v` flag** shows verbose output (each test name).

**Run specific class:**
```bash
pytest tests/ -k "TestHealthEndpoint"
```

**Run with coverage:**
```bash
pytest tests/ --cov=app
```

---

## Test Patterns Used

### Pattern 1: Arrange-Act-Assert

Every test follows this structure:

```python
def test_create_item_with_name_and_description(self):
    # ARRANGE - Set up test data
    item_data = {"name": "Laptop", "description": "MacBook Pro"}

    # ACT - Perform the action
    response = client.post("/items", json=item_data)

    # ASSERT - Verify the result
    assert response.status_code == 201
    assert response.json()["name"] == "Laptop"
```

### Pattern 2: Testing Happy Path and Error Cases

**Happy path:** What happens when everything is correct
```python
def test_create_item_with_name_and_description(self):
    response = client.post("/items", json={"name": "Laptop", "description": "Test"})
    assert response.status_code == 201  # Success!
```

**Error case:** What happens when something is wrong
```python
def test_create_item_without_name_fails(self):
    response = client.post("/items", json={"description": "No name"})
    assert response.status_code == 422  # Validation error!
```

**Both are equally important!**

### Pattern 3: Boundary Testing

Test the edges of valid input:

```python
def test_name_max_length_validation(self):
    long_name = "a" * 101  # One character over the limit
    response = client.post("/items", json={"name": long_name})
    assert response.status_code == 422  # Should fail

def test_valid_max_length_name_succeeds(self):
    max_name = "a" * 100  # Exactly at the limit
    response = client.post("/items", json={"name": max_name})
    assert response.status_code == 201  # Should pass
```

---

## What Makes These Tests "Production-Ready"

### 1. Test Isolation
Each test is independent. Running tests in any order gives the same result.

### 2. Comprehensive Coverage
We test:
- Success cases (happy path)
- Error cases (validation failures)
- Edge cases (boundary values)
- Response format (API contract)

### 3. Clear Naming
Test names describe what they test:
- `test_create_item_with_name_and_description` ✓
- `test_1` ✗

### 4. Organized Structure
Tests grouped by endpoint/feature, not randomly scattered.

---

## Common Testing Mistakes to Avoid

### Mistake 1: No test isolation
**Problem:** Tests pass individually but fail when run together
**Fix:** Use fixtures to reset state before each test

### Mistake 2: Only testing happy path
**Problem:** Code works for valid input but crashes on invalid input
**Fix:** Test error cases and edge cases equally

### Mistake 3: Testing implementation, not behavior
**Problem:** Tests break when you refactor even if behavior is unchanged
**Fix:** Test what the API returns, not how it internally works

### Mistake 4: No assertions
**Problem:** Test runs without errors but doesn't actually verify anything
**Fix:** Every test should have at least one `assert` statement

### Mistake 5: Hardcoded test order
**Problem:** Test 2 relies on data created by Test 1
**Fix:** Each test should set up its own data

---

## Why This Matters for Your Career

**Basic project:** "I built an API" (no proof it works)

**Production-ready project:** "I built an API with 20+ automated tests covering success cases, error handling, and validation"

**In interviews:**
- "How do you ensure code quality?" → "Automated tests with pytest"
- "How do you prevent regressions?" → "CI runs tests on every push"
- "What's your testing strategy?" → "Unit tests for each endpoint, covering happy path and error cases"

---

## Production-Ready Checklist (Phase 2)

✅ **Test framework** - Pytest configured and working
✅ **Test isolation** - Fixtures reset state between tests
✅ **Happy path tests** - All endpoints tested with valid data
✅ **Error case tests** - Validation errors tested
✅ **Boundary tests** - Edge cases for min/max values
✅ **Response format tests** - API contract verified
✅ **Organized structure** - Tests grouped logically
✅ **Clear naming** - Test names describe what they test
✅ **Fast execution** - All tests run in under 1 second

---

## Key Takeaway

**Phase 2 proves your code works.**

Anyone can write code that "seems to work." Professionals write code with automated tests that **prove** it works - and will keep working as the codebase grows.

Tests are not optional. They're the foundation of professional software development.

---

## Next Steps

With tests in place, Phase 3 adds **linting and code formatting** to ensure consistent code quality across the project.
