"""Pydantic models for request/response validation."""

from pydantic import BaseModel, Field


class ItemCreate(BaseModel):
    """Item creation request."""

    name: str = Field(..., min_length=1, max_length=100, description="Item name")
    description: str | None = Field(None, max_length=500, description="Item description")

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
    """Item with ID."""

    id: int = Field(..., description="Item ID")
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
