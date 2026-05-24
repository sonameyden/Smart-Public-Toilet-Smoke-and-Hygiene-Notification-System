"""
Unit tests for sensor_service.
All DB and cache calls are mocked — no Supabase connection required.
"""
from unittest.mock import MagicMock, patch
import pytest

from app.domain.sensor import (
    SensorReading,
    DEFAULT_SMOKE_THRESHOLD,
    DEFAULT_GAS_THRESHOLD,
    DEFAULT_AIR_QUALITY_THRESHOLD,
)


# ── Domain logic tests (pure, no mocks needed) ───────────────────────────────

class TestSensorReadingDomain:
    def _reading(self, smoke=10, gas=40, air=90):
        return SensorReading(
            smoke_ppm=smoke, gas_ppm=gas, air_quality=air,
            temperature=24.0, humidity=55.0,
        )

    def test_no_alert_under_threshold(self):
        r = self._reading()
        assert not r.is_smoke_alert()
        assert not r.is_gas_alert()
        assert not r.is_hygiene_warning()

    def test_smoke_alert_over_threshold(self):
        assert self._reading(smoke=DEFAULT_SMOKE_THRESHOLD + 1).is_smoke_alert()

    def test_gas_alert_over_threshold(self):
        assert self._reading(gas=DEFAULT_GAS_THRESHOLD + 1).is_gas_alert()

    def test_hygiene_warning_below_threshold(self):
        assert self._reading(air=DEFAULT_AIR_QUALITY_THRESHOLD - 1).is_hygiene_warning()

    def test_custom_threshold_respected(self):
        r = self._reading(smoke=60)
        assert r.is_smoke_alert(threshold=50)
        assert not r.is_smoke_alert(threshold=70)


# ── Service-level tests (mock repos + cache) ─────────────────────────────────

class TestGetLatest:
    @patch("app.services.sensor_service.sensor_cache")
    @patch("app.services.sensor_service.sensor_repository")
    @patch("app.services.sensor_service.get_settings")
    def test_returns_cached_value_without_hitting_db(
        self, mock_settings, mock_repo, mock_cache
    ):
        mock_cache.get_latest.return_value = {
            "smoke_ppm": 12.0, "gas_ppm": 45.0, "air_quality": 92.0,
            "temperature": 24.0, "humidity": 58.0,
            "location": "IT Building Ground Floor", "recorded_at": None,
            "smoke_status": "normal", "gas_status": "normal",
            "air_quality_status": "normal",
        }
        from app.services.sensor_service import get_latest
        result = get_latest()
        assert result is not None
        assert result.smoke_ppm == 12.0
        mock_repo.get_latest.assert_not_called()

    @patch("app.services.sensor_service.sensor_cache")
    @patch("app.services.sensor_service.sensor_repository")
    @patch("app.services.sensor_service.get_settings")
    def test_falls_back_to_db_on_cache_miss(
        self, mock_settings, mock_repo, mock_cache
    ):
        mock_cache.get_latest.return_value = None
        mock_repo.get_latest.return_value = {
            "id": 1, "smoke_ppm": 20.0, "gas_ppm": 50.0, "air_quality": 85.0,
            "temperature": 25.0, "humidity": 60.0,
            "location": "IT Building Ground Floor", "recorded_at": None,
        }
        mock_settings.return_value = MagicMock(
            smoke_threshold=50, gas_threshold=100, air_quality_threshold=70
        )
        from app.services.sensor_service import get_latest
        result = get_latest()
        assert result.smoke_ppm == 20.0
        mock_repo.get_latest.assert_called_once()
        mock_cache.set_latest.assert_called_once()

    @patch("app.services.sensor_service.sensor_cache")
    @patch("app.services.sensor_service.sensor_repository")
    def test_returns_none_when_no_data(self, mock_repo, mock_cache):
        mock_cache.get_latest.return_value = None
        mock_repo.get_latest.return_value = None
        from app.services.sensor_service import get_latest
        assert get_latest() is None
