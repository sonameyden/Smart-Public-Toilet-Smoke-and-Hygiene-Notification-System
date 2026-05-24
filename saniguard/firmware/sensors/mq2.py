"""
MQ-2 Smoke Sensor Driver for Raspberry Pi Pico W (MicroPython).
Converts ADC reading to approximate PPM using the MQ-2 sensitivity curve.
"""
import math
from machine import ADC, Pin


class MQ2:
    """
    Wiring:
        VCC  -> 3.3V (Pico pin 36)
        GND  -> GND
        AOUT -> GP26 (ADC0)
    """
    _A       = 574.25   # sensitivity curve coefficient
    _B       = -2.222   # sensitivity curve exponent
    _ADC_MAX = 65535
    _VCC     = 3.3
    _RL      = 10.0     # load resistance in kΩ

    def __init__(self, adc_pin: int, r0: float = 9.83):
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

    def read_raw(self) -> int:
        return self._adc.read_u16()
