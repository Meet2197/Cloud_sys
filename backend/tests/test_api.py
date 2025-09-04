import pytest
from httpx import AsyncClient
from main import app

@pytest.mark.asyncio
async def test_read_files(tmp_path):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/files/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_create_file():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/files/", json={
            "name": "demo.txt",
            "type": "text",
            "metadata": {"tag": "seed"}
        })
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "demo.txt"
