"""Integration tests for /auth routes using httpx + mocked DB."""
import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import patch
from app.main import app

_MOCK_USER = {
    "id": "user-uuid-001",
    "full_name": "Test Admin",
    "email": "test@campus.edu",
    "password_hash": "$2b$12$KIXhg4rPIYVLb3W0l5FNAuMx7pF9G0ePdMh3CkPqVDnHkBpLfSwCy",
    "role": "admin",
    "is_active": True,
    "last_login": None,
    "created_at": "2026-01-01T00:00:00",
}


@pytest.fixture
def client():
    return AsyncClient(transport=ASGITransport(app=app), base_url="http://test")


@pytest.mark.asyncio
class TestLoginRoute:
    @patch("app.services.auth_service.user_repository")
    @patch("app.services.auth_service.verify_password", return_value=True)
    async def test_login_success(self, mock_verify, mock_repo, client):
        mock_repo.get_by_email.return_value = _MOCK_USER
        mock_repo.update_last_login.return_value = None
        async with client as c:
            resp = await c.post(
                "/api/v1/auth/login",
                json={"email": "test@campus.edu", "password": "password123"},
            )
        assert resp.status_code == 200
        assert "access_token" in resp.json()
        assert resp.json()["role"] == "admin"

    @patch("app.services.auth_service.user_repository")
    async def test_login_wrong_email(self, mock_repo, client):
        mock_repo.get_by_email.return_value = None
        async with client as c:
            resp = await c.post(
                "/api/v1/auth/login",
                json={"email": "nobody@campus.edu", "password": "wrong"},
            )
        assert resp.status_code == 401

    @patch("app.services.auth_service.user_repository")
    @patch("app.services.auth_service.verify_password", return_value=False)
    async def test_login_wrong_password(self, mock_verify, mock_repo, client):
        mock_repo.get_by_email.return_value = _MOCK_USER
        async with client as c:
            resp = await c.post(
                "/api/v1/auth/login",
                json={"email": "test@campus.edu", "password": "wrongpass"},
            )
        assert resp.status_code == 401


@pytest.mark.asyncio
class TestRegisterRoute:
    @patch("app.services.auth_service.user_repository")
    async def test_register_success(self, mock_repo, client):
        mock_repo.get_by_email.return_value = None
        mock_repo.create.return_value = {**_MOCK_USER, "email": "new@campus.edu"}
        async with client as c:
            resp = await c.post(
                "/api/v1/auth/register",
                json={"full_name": "New User", "email": "new@campus.edu",
                      "password": "securepass", "role": "viewer"},
            )
        assert resp.status_code == 201
        assert "access_token" in resp.json()

    @patch("app.services.auth_service.user_repository")
    async def test_register_duplicate_email(self, mock_repo, client):
        mock_repo.get_by_email.return_value = _MOCK_USER
        async with client as c:
            resp = await c.post(
                "/api/v1/auth/register",
                json={"full_name": "Dupe", "email": "test@campus.edu",
                      "password": "pass", "role": "viewer"},
            )
        assert resp.status_code == 409
