import pytest
import httpx

DISCOVERY_URL = "http://localhost:8500"

@pytest.mark.asyncio
async def test_discovery_register():
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{DISCOVERY_URL}/register", json={
            "name": "test-discovery",
            "port": 1234,
            "ttl": 15
        })
        assert response.status_code == 200
        assert "registered" in response.json()["message"].lower()