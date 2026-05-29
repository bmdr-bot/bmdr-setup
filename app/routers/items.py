"""Example CRUD router — demonstrates API patterns."""

import logging
from typing import List, Optional

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/items", tags=["items"])


# In-memory store (replace with database in production)
items_db = {}
next_id = 1


class ItemCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    price: float = Field(..., gt=0)
    tags: List[str] = Field(default_factory=list)


class Item(ItemCreate):
    id: int


class ItemUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    price: Optional[float] = Field(None, gt=0)
    tags: Optional[List[str]] = None


@router.get("/", response_model=List[Item], summary="List all items")
async def list_items(skip: int = 0, limit: int = 100):
    """List items with pagination."""
    item_list = list(items_db.values())
    return item_list[skip : skip + limit]


@router.post(
    "/",
    response_model=Item,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new item",
)
async def create_item(item: ItemCreate):
    """Create a new item."""
    global next_id
    item_id = next_id
    next_id += 1

    item_dict = item.model_dump()
    item_dict["id"] = item_id
    items_db[item_id] = item_dict

    logger.info(f"Created item {item_id}: {item.name}")
    return item_dict


@router.get("/{item_id}", response_model=Item, summary="Get item by ID")
async def get_item(item_id: int):
    """Get a specific item by ID."""
    if item_id not in items_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item {item_id} not found",
        )
    return items_db[item_id]


@router.put("/{item_id}", response_model=Item, summary="Update item")
async def update_item(item_id: int, item_update: ItemUpdate):
    """Update an existing item."""
    if item_id not in items_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item {item_id} not found",
        )

    stored = items_db[item_id]
    update_data = item_update.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        stored[field] = value

    logger.info(f"Updated item {item_id}")
    return stored


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete item")
async def delete_item(item_id: int):
    """Delete an item."""
    if item_id not in items_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item {item_id} not found",
        )

    del items_db[item_id]
    logger.info(f"Deleted item {item_id}")
    return None
