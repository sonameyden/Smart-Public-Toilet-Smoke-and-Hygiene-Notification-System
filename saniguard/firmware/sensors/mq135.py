"""
MQ-135 Air Quality / Gas Sensor Driver for Raspberry Pi Pico W (MicroPython).
Measures CO2, NH3, benzene, alcohol, smoke.
Outputs both raw PPM and a 0-100 air quality score (100 = cleanest).
"""
import math
from machine import ADC, Pin


class MQ135:
    """
    Wiring:
        VCC  -> 3.3V
        GND  -> GND
        AOUT -> GP27 (ADC1)
    """
    _A       = 116.60   # sensitivity curve coefficient for air quality
    _B       = -2.769   # sensitivity curve exponent
    _ADC_MAX = 65535
    _VCC     = 3.3
    _RL      = 10.0     # load resistance in kΩ
    _PPM_CLEAN_AIR = 400.0  # ~400 ppm CO2 is normal outdoor air

    def __init__(self, adc_pin: int, r0: float = 3.68):
        self._adc = ADC(Pin(adc_pin))
        self._r0  = r0

    def _read_rs(self) -> float:
        raw     = self._adc.read_u16()
        voltage = (raw / self._ADC_MAX) * self._VCC
        if voltage <= 0:
            return 0.0
        return ((self._VCC - voltage) / voltage) * self._RL

    def read_ppm(self) -> float:
        rs = self._read_rs()
        if rs <= 0 or self._r0 <= 0:
            return 0.0
        ppm = self._A * math.pow(rs / self._r0, self._B)
        return round(max(ppm, 0.0), 2)

    def read_air_quality_score(self) -> float:
        """
        Convert PPM to a 0-100 quality score.
        400 ppm (clean air) -> 100
        2000+ ppm           -> ~0
        """
        ppm = self.read_ppm()
        ppm = max(ppm, self._PPM_CLEAN_AIR)
        score = 100.0 - ((ppm - self._PPM_CLEAN_AIR) / 80.0)
        return round(max(0.0, min(100.0, score)), 1)

    def read_raw(self) -> int:
        return self._adc.read_u16()
