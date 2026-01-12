"""Pydantic models for request/response validation."""

from pydantic import BaseModel, Field


class ItemCreate(BaseModel):
    """Model for creating a new item."""

    name: str = Field(..., min_length=1, max_length=100, description="Item name (required)")
    description: str | None = Field(None, max_length=500, description="Item description (optional)")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Example Item",
                    "description": "This is an example item description",
                }
            ]
        }
    }


class Item(BaseModel):
    """Model representing an item with an ID."""

    id: int = Field(..., description="Unique item identifier")
    name: str = Field(..., description="Item name")
    description: str | None = Field(None, description="Item description")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "name": "Example Item",
                    "description": "This is an example item description",
                }
            ]
        }
    }


class HealthResponse(BaseModel):
    """Health check response model."""

    status: str = Field(..., description="Service health status")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "status": "ok",
                }
            ]
        }
    }
