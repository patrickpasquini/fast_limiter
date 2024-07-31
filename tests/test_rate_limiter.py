import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI, status, Depends
from fast_limiter import FastLimiter
from unittest.mock import AsyncMock

app = FastAPI()

mock_storage = AsyncMock()
mock_storage.get_timestamp.return_value = 0.1
mock_storage.get_remaining.return_value = 2

limiter = FastLimiter(mock_storage, limit=3, interval=5)


@app.get("/rate-limit", dependencies=[Depends(limiter)])
async def rate_limit_route():
    return {"detail": "Welcome to limit route"}


client = TestClient(app)


@pytest.mark.asyncio
async def test_limit_route_pass():
    response = client.get("/rate-limit")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_decorator_limit_route_exceed_limit():
    mock_storage.get_remaining.return_value = 0
    response = client.get("/rate-limit")
    assert response.status_code == status.HTTP_429_TOO_MANY_REQUESTS
