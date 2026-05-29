from dataclasses import dataclass
from datetime import datetime
from typing import Optional


# Default detection thresholds — overridden by system_settings table at runtime
DEFAULT_SMOKE_THRESHOLD = 150.0      # ppm
DEFAULT_GAS_THRESHOLD = 100.0       # ppm
DEFAULT_AIR_QUALITY_THRESHOLD = 70  # score (below this = warning)


@dataclass
class SensorReading:
    smoke_ppm: float
    gas_ppm: float
    air_quality: float
    temperature: float
    humidity: float
    location: str = "IT Building Ground Floor"
    recorded_at: Optional[datetime] = None

    def is_smoke_alert(self, threshold: float = DEFAULT_SMOKE_THRESHOLD) -> bool:
        return self.smoke_ppm > threshold

    def is_gas_alert(self, threshold: float = DEFAULT_GAS_THRESHOLD) -> bool:
        return self.gas_ppm > threshold

    def is_hygiene_warning(self, threshold: float = DEFAULT_AIR_QUALITY_THRESHOLD) -> bool:
        return self.air_quality < threshold
