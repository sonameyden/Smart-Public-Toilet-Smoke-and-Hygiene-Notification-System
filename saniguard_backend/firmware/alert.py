from machine import Pin, PWM
import time


class LocalAlert:
    def __init__(self, buzzer_pin: int, led_red_pin: int, led_green_pin: int):
        self._buzzer      = PWM(Pin(buzzer_pin))
        self._led_red     = Pin(led_red_pin, Pin.OUT)
        self._led_green   = Pin(led_green_pin, Pin.OUT)
        self._buzzer.duty_u16(0)
        self._led_red.off()
        self._led_green.on()   # green on by default = safe

    def smoke_alert(self) -> None:
        """Three sharp beeps + red LED for smoke detection."""
        self._led_green.off()
        self._led_red.on()
        for _ in range(3):
            self._beep(frequency=2000, duration_ms=200)
            time.sleep_ms(100)

    def hygiene_warning(self) -> None:
        """One long low beep + red LED for hygiene/gas warning."""
        self._led_green.off()
        self._led_red.on()
        self._beep(frequency=1000, duration_ms=600)

    def clear(self) -> None:
        """All clear — green on, red off, buzzer off."""
        self._led_red.off()
        self._led_green.on()
        self._buzzer.duty_u16(0)

    def _beep(self, frequency: int, duration_ms: int) -> None:
        self._buzzer.freq(frequency)
        self._buzzer.duty_u16(32768)
        time.sleep_ms(duration_ms)
        self._buzzer.duty_u16(0)

