"""Tests for items endpoints."""

import pytest
from httpx import AsyncClient

from app.main import app


@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_create_item(client):
    item = {
        "name": "Test Item",
        "description": "A test item",
        "price": 9.99,
        "tags": ["test", "demo"],
    }
    response = await client.post("/items/", json=item)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == item["name"]
    assert data["price"] == item["price"]
    assert "id" in data


@pytest.mark.asyncio
async def test_list_items(client):
    response = await client.get("/items/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


@pytest.mark.asyncio
async def test_get_item(client):
    # Create item first
    item = {"name": "Get Test", "price": 5.0}
    create_resp = await client.post("/items/", json=item)
    created = create_resp.json()

    # Get it
    response = await client.get(f"/items/{created['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == item["name"]


@pytest.mark.asyncio
async def test_get_item_not_found(client):
    response = await client.get("/items/99999")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_item(client):
    # Create item
    item = {"name": "Update Test", "price": 10.0}
    create_resp = await client.post("/items/", json=item)
    created = create_resp.json()

    # Update it
    update = {"name": "Updated Name"}
    response = await client.put(f"/items/{created['id']}", json=update)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Name"
    assert data["price"] == 10.0  # Unchanged


@pytest.mark.asyncio
async def test_delete_item(client):
    # Create item
    item = {"name": "Delete Test", "price": 15.0}
    create_resp = await client.post("/items/", json=item)
    created = create_resp.json()

    # Delete it
    response = await client.delete(f"/items/{created['id']}")
    assert response.status_code == 204

    # Verify it's gone
    get_resp = await client.get(f"/items/{created['id']}")
    assert get_resp.status_code == 404
