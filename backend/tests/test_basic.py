import asyncio
import os
import pytest
from httpx import AsyncClient
from app.main import app
from app.database import Base, engine, SessionLocal
from app import models

@pytest.fixture(scope='module')
def anyio_backend():
    return 'asyncio'

@pytest.fixture(scope='module', autouse=True)
def prepare_db():
    # Ensure a fresh sqlite DB for tests
    db_path = os.getenv('TEST_DB', 'data/test_app.db')
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    # point env var for engine - for tests we recreate engine via DATABASE_URL env var not easily changed here
    # instead drop and recreate tables on the existing engine
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.mark.anyio
async def test_create_and_list_folder():
    async with AsyncClient(app=app, base_url='http://test') as ac:
        resp = await ac.post('/folders/', json={'name':'TestFolder', 'parent_id': None})
        assert resp.status_code == 200
        data = resp.json()
        assert data['name'] == 'TestFolder'

        resp2 = await ac.get('/folders/')
        assert resp2.status_code == 200
        assert any(f['name']=='TestFolder' for f in resp2.json())

@pytest.mark.anyio
async def test_recluster_empty():
    async with AsyncClient(app=app, base_url='http://test') as ac:
        # call recluster on empty DB - should succeed
        resp = await ac.post('/analytics/recluster')
        assert resp.status_code == 200
        body = resp.json()
        assert 'nodes' in body and 'edges' in body

