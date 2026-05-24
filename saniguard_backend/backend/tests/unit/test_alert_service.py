"""Unit tests for alert_service."""
from unittest.mock import patch
import pytest
from app.domain.alert import AlertType, AlertSeverity, AlertStatus


class TestAlertDomain:
    def _alert(self, status=AlertStatus.ACTIVE):
        from app.domain.alert import Alert
        from datetime import datetime
        return Alert(
            id="test-id", type=AlertType.SMOKE, severity=AlertSeverity.HIGH,
            status=status, title="Smoke Detected", description="Test",
            location="IT Building Ground Floor", created_at=datetime.utcnow(),
        )

    def test_active_alert_is_active(self):
        assert self._alert(AlertStatus.ACTIVE).is_active()

    def test_resolved_alert_is_not_active(self):
        assert not self._alert(AlertStatus.RESOLVED).is_active()

    def test_resolve_mutates_status(self):
        alert = self._alert(AlertStatus.ACTIVE)
        alert.resolve("user-123")
        assert alert.status == AlertStatus.RESOLVED
        assert alert.resolved_by == "user-123"
        assert alert.resolved_at is not None


class TestGetActiveCount:
    @patch("app.services.alert_service.alert_cache")
    @patch("app.services.alert_service.alert_repository")
    def test_returns_cached_count(self, mock_repo, mock_cache):
        mock_cache.get_active_count.return_value = 3
        from app.services.alert_service import get_active_count
        assert get_active_count() == 3
        mock_repo.count_active.assert_not_called()

    @patch("app.services.alert_service.alert_cache")
    @patch("app.services.alert_service.alert_repository")
    def test_queries_db_on_cache_miss(self, mock_repo, mock_cache):
        mock_cache.get_active_count.return_value = None
        mock_repo.count_active.return_value = 5
        from app.services.alert_service import get_active_count
        assert get_active_count() == 5
        mock_cache.set_active_count.assert_called_once_with(5)


class TestResolveAlert:
    @patch("app.services.alert_service.ws_manager")
    @patch("app.services.alert_service.analytics_cache")
    @patch("app.services.alert_service.alert_cache")
    @patch("app.services.alert_service.alert_repository")
    def test_resolve_invalidates_cache(
        self, mock_repo, mock_alert_cache, mock_analytics_cache, mock_ws
    ):
        from datetime import datetime
        ts = datetime.utcnow().isoformat()
        mock_repo.get_by_id.return_value = {
            "id": "abc", "status": "active", "type": "smoke",
            "severity": "high", "title": "Test", "description": "Test",
            "location": "IT Building", "created_at": ts,
        }
        mock_repo.resolve.return_value = {
            "id": "abc", "status": "resolved", "type": "smoke",
            "severity": "high", "title": "Test", "description": "Test",
            "location": "IT Building", "created_at": ts,
            "resolved_by": "user-1", "resolved_at": ts,
        }
        from app.services.alert_service import resolve_alert
        resolve_alert("abc", "user-1", "admin")
        mock_alert_cache.invalidate.assert_called_once()
        mock_analytics_cache.invalidate_all.assert_called_once()

    @patch("app.services.alert_service.alert_repository")
    def test_raises_not_found_for_missing_alert(self, mock_repo):
        mock_repo.get_by_id.return_value = None
        from app.services.alert_service import resolve_alert
        from app.core.exceptions import NotFoundError
        with pytest.raises(NotFoundError):
            resolve_alert("nonexistent", "user-1", "admin")
