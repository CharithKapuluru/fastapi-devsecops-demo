"""FastAPI application with health and items endpoints."""

from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse

from app.config import logger, settings
from app.models import HealthResponse, Item, ItemCreate

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="FastAPI microservice with DevSecOps best practices",
)

# In-memory storage
items_db: dict[int, Item] = {}
next_item_id: list[int] = [1]


@app.get("/health", response_model=HealthResponse, status_code=status.HTTP_200_OK)
async def health_check() -> HealthResponse:
    """Health check endpoint."""
    logger.info("Health check requested")
    return HealthResponse(status="ok")


@app.get("/items", response_model=list[Item], status_code=status.HTTP_200_OK)
async def get_items() -> list[Item]:
    """Get all items."""
    logger.info(f"Get items requested - returning {len(items_db)} items")
    return list(items_db.values())


@app.post("/items", response_model=Item, status_code=status.HTTP_201_CREATED)
async def create_item(item_data: ItemCreate) -> Item:
    """Create a new item with auto-incrementing ID."""
    try:
        current_id = next_item_id[0]

        new_item = Item(
            id=current_id,
            name=item_data.name,
            description=item_data.description,
        )

        items_db[current_id] = new_item
        logger.info(f"Created item with ID {current_id}: {item_data.name}")

        next_item_id[0] += 1

        return new_item

    except Exception as e:
        logger.error(f"Failed to create item: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create item",
        ) from e


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler."""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An internal error occurred"},
    )
