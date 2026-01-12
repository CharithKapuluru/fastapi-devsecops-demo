"""FastAPI application with health and items endpoints."""

from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse

from app.config import logger, settings
from app.models import HealthResponse, Item, ItemCreate

# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="Production-ready FastAPI microservice with DevSecOps best practices",
)

# In-memory storage for items (MVP - no database yet)
items_db: dict[int, Item] = {}
# Use list to make ID counter mutable (allows resetting in tests)
next_item_id: list[int] = [1]


@app.get("/health", response_model=HealthResponse, status_code=status.HTTP_200_OK)
async def health_check() -> HealthResponse:
    """
    Health check endpoint.

    Returns:
        HealthResponse: Service health status
    """
    logger.info("Health check requested")
    return HealthResponse(status="ok")


@app.get("/items", response_model=list[Item], status_code=status.HTTP_200_OK)
async def get_items() -> list[Item]:
    """
    Get all items.

    Returns:
        list[Item]: List of all items
    """
    logger.info(f"Get items requested - returning {len(items_db)} items")
    return list(items_db.values())


@app.post("/items", response_model=Item, status_code=status.HTTP_201_CREATED)
async def create_item(item_data: ItemCreate) -> Item:
    """
    Create a new item.

    Args:
        item_data: Item data with name (required) and description (optional)

    Returns:
        Item: The created item with assigned ID

    Raises:
        HTTPException: If item creation fails
    """
    try:
        # Get current ID
        current_id = next_item_id[0]

        # Create new item with auto-incrementing ID
        new_item = Item(
            id=current_id,
            name=item_data.name,
            description=item_data.description,
        )

        # Store in database
        items_db[current_id] = new_item
        logger.info(f"Created item with ID {current_id}: {item_data.name}")

        # Increment ID counter
        next_item_id[0] += 1

        return new_item

    except Exception as e:
        logger.error(f"Failed to create item: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create item",
        )


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """
    Global exception handler for unhandled errors.

    Returns generic error message to avoid leaking internal details.
    """
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An internal error occurred"},
    )
