# auth_system/tests/test_auth.py
import pytest
from httpx import AsyncClient
from auth_system.main import app

@pytest.mark.asyncio
async def test_register():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/register", json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "Test1234!",
            "confirm_password": "Test1234!"
        })
        assert response.status_code == 200
        assert response.json() == {"message": "User created successfully"}

@pytest.mark.asyncio
async def test_login():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/login", data={
            "username": "testuser",
            "password": "Test1234!"
        })
        assert response.status_code == 200
        assert "access_token" in response.json()
        assert "refresh_token" in response.json()