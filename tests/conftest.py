"""Pytest configuration and shared fixtures."""

import pytest
from httpx import AsyncClient

from app.main import app


@pytest.fixture
async def client():
    """Async HTTP client for testing."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
