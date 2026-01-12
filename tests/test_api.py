"""Tests for FastAPI endpoints."""

import pytest
from fastapi.testclient import TestClient

from app.main import app, items_db, next_item_id


@pytest.fixture(autouse=True)
def reset_items_db():
    """Reset the in-memory database before each test.

    This ensures test isolation - each test starts with a clean slate.
    """
    # Clear all items from the database
    items_db.clear()

    # Reset the ID counter to 1
    next_item_id[0] = 1

    yield  # Run the test

    # Cleanup after test (optional, but good practice)
    items_db.clear()
    next_item_id[0] = 1


# Create a test client
client = TestClient(app)


class TestHealthEndpoint:
    """Tests for the health check endpoint."""

    def test_health_check_returns_ok(self):
        """Test that GET /health returns status ok."""
        response = client.get("/health")

        # Check status code
        assert response.status_code == 200

        # Check response body
        assert response.json() == {"status": "ok"}

    def test_health_check_returns_json(self):
        """Test that health endpoint returns JSON content type."""
        response = client.get("/health")

        assert response.headers["content-type"] == "application/json"


class TestGetItemsEndpoint:
    """Tests for GET /items endpoint."""

    def test_get_items_empty_list(self):
        """Test that GET /items returns empty list when no items exist."""
        response = client.get("/items")

        # Check status code
        assert response.status_code == 200

        # Check it returns an empty list
        assert response.json() == []

    def test_get_items_with_data(self):
        """Test that GET /items returns items after they are created."""
        # First, create an item
        create_response = client.post(
            "/items",
            json={"name": "Test Item", "description": "Test description"}
        )
        assert create_response.status_code == 201

        # Now get all items
        response = client.get("/items")

        assert response.status_code == 200
        items = response.json()

        # Should have 1 item
        assert len(items) == 1

        # Check the item data
        assert items[0]["name"] == "Test Item"
        assert items[0]["description"] == "Test description"
        assert items[0]["id"] == 1

    def test_get_items_returns_multiple_items(self):
        """Test that GET /items returns all items when multiple exist."""
        # Create 3 items
        client.post("/items", json={"name": "Item 1", "description": "First"})
        client.post("/items", json={"name": "Item 2", "description": "Second"})
        client.post("/items", json={"name": "Item 3"})

        # Get all items
        response = client.get("/items")

        assert response.status_code == 200
        items = response.json()

        # Should have 3 items
        assert len(items) == 3

        # Check IDs are sequential
        assert items[0]["id"] == 1
        assert items[1]["id"] == 2
        assert items[2]["id"] == 3


class TestPostItemsEndpoint:
    """Tests for POST /items endpoint."""

    def test_create_item_with_name_and_description(self):
        """Test creating an item with both name and description."""
        item_data = {
            "name": "Laptop",
            "description": "MacBook Pro 16-inch"
        }

        response = client.post("/items", json=item_data)

        # Check status code (201 Created)
        assert response.status_code == 201

        # Check response data
        data = response.json()
        assert data["id"] == 1
        assert data["name"] == "Laptop"
        assert data["description"] == "MacBook Pro 16-inch"

    def test_create_item_with_only_name(self):
        """Test creating an item with only name (description optional)."""
        item_data = {
            "name": "Phone"
        }

        response = client.post("/items", json=item_data)

        assert response.status_code == 201

        data = response.json()
        assert data["id"] == 1
        assert data["name"] == "Phone"
        assert data["description"] is None  # Should be None when not provided

    def test_create_item_without_name_fails(self):
        """Test that creating an item without name returns validation error."""
        item_data = {
            "description": "This has no name"
        }

        response = client.post("/items", json=item_data)

        # Should return 422 Unprocessable Entity (validation error)
        assert response.status_code == 422

        # Check error details
        error = response.json()
        assert "detail" in error

        # Check that the error mentions the missing 'name' field
        assert any(
            err["loc"] == ["body", "name"] and err["type"] == "missing"
            for err in error["detail"]
        )

    def test_create_item_with_empty_name_fails(self):
        """Test that creating an item with empty name fails validation."""
        item_data = {
            "name": "",  # Empty string
            "description": "Empty name"
        }

        response = client.post("/items", json=item_data)

        # Should fail validation (name must be min 1 character)
        assert response.status_code == 422

    def test_create_item_with_invalid_type_fails(self):
        """Test that creating an item with wrong data type fails."""
        item_data = {
            "name": 12345,  # Should be string, not number
            "description": "Wrong type"
        }

        response = client.post("/items", json=item_data)

        # Should return validation error
        assert response.status_code == 422

    def test_create_item_auto_increments_id(self):
        """Test that item IDs auto-increment correctly."""
        # Create first item
        response1 = client.post("/items", json={"name": "First"})
        assert response1.json()["id"] == 1

        # Create second item
        response2 = client.post("/items", json={"name": "Second"})
        assert response2.json()["id"] == 2

        # Create third item
        response3 = client.post("/items", json={"name": "Third"})
        assert response3.json()["id"] == 3

    def test_create_item_is_retrievable(self):
        """Test that a created item can be retrieved via GET /items."""
        # Create an item
        create_data = {"name": "Retrievable Item", "description": "Test"}
        create_response = client.post("/items", json=create_data)
        created_item = create_response.json()

        # Get all items
        get_response = client.get("/items")
        items = get_response.json()

        # The created item should be in the list
        assert len(items) == 1
        assert items[0] == created_item


class TestItemValidation:
    """Tests for item data validation rules."""

    def test_name_max_length_validation(self):
        """Test that name exceeding max length fails validation."""
        # Name should be max 100 characters
        long_name = "a" * 101  # 101 characters

        response = client.post(
            "/items",
            json={"name": long_name}
        )

        assert response.status_code == 422

    def test_description_max_length_validation(self):
        """Test that description exceeding max length fails validation."""
        # Description should be max 500 characters
        long_description = "a" * 501  # 501 characters

        response = client.post(
            "/items",
            json={"name": "Valid Name", "description": long_description}
        )

        assert response.status_code == 422

    def test_valid_max_length_name_succeeds(self):
        """Test that name at exactly max length (100 chars) works."""
        max_name = "a" * 100  # Exactly 100 characters

        response = client.post(
            "/items",
            json={"name": max_name}
        )

        assert response.status_code == 201
        assert response.json()["name"] == max_name

    def test_valid_max_length_description_succeeds(self):
        """Test that description at exactly max length (500 chars) works."""
        max_description = "a" * 500  # Exactly 500 characters

        response = client.post(
            "/items",
            json={"name": "Test", "description": max_description}
        )

        assert response.status_code == 201
        assert response.json()["description"] == max_description


class TestAPIResponseFormat:
    """Tests for API response formats and structure."""

    def test_all_endpoints_return_json(self):
        """Test that all endpoints return JSON content type."""
        # Test health endpoint
        response = client.get("/health")
        assert "application/json" in response.headers["content-type"]

        # Test get items
        response = client.get("/items")
        assert "application/json" in response.headers["content-type"]

        # Test post items
        response = client.post("/items", json={"name": "Test"})
        assert "application/json" in response.headers["content-type"]

    def test_created_item_has_all_fields(self):
        """Test that created item response includes all expected fields."""
        response = client.post(
            "/items",
            json={"name": "Complete Item", "description": "Full test"}
        )

        data = response.json()

        # Check all required fields exist
        assert "id" in data
        assert "name" in data
        assert "description" in data

        # Check field types
        assert isinstance(data["id"], int)
        assert isinstance(data["name"], str)
        assert isinstance(data["description"], str) or data["description"] is None
