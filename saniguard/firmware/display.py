"""
OLED SSD1306 128x64 display driver wrapper (optional).
Uses MicroPython's ssd1306 library via I2C.
If no OLED is connected, all methods silently do nothing.
"""
from machine import Pin, I2C


class OLEDDisplay:
    """
    Wiring:
        VCC -> 3.3V
        GND -> GND
        SDA -> GP4
        SCL -> GP5
    """

    def __init__(self, sda_pin: int, scl_pin: int, width: int = 128, height: int = 64):
        self._available = False
        try:
            import ssd1306
            i2c = I2C(0, sda=Pin(sda_pin), scl=Pin(scl_pin), freq=400_000)
            self._oled = ssd1306.SSD1306_I2C(width, height, i2c)
            self._available = True
        except Exception as e:
            print("OLED not available:", e)

    def show_readings(self, smoke: float, gas: float, air: float, temp: float, hum: float) -> None:
        if not self._available:
            return
        self._oled.fill(0)
        self._oled.text("Saniguard", 24, 0)
        self._oled.text("Smoke:{:.1f}ppm".format(smoke),  0, 16)
        self._oled.text("Gas:  {:.1f}ppm".format(gas),    0, 26)
        self._oled.text("Air:  {:.0f}%".format(air),      0, 36)
        self._oled.text("Temp: {:.1f}C".format(temp),     0, 46)
        self._oled.text("Hum:  {:.0f}%".format(hum),      0, 56)
        self._oled.show()

    def show_alert(self, message: str) -> None:
        if not self._available:
            return
        self._oled.fill(0)
        self._oled.text("!! ALERT !!", 16, 20)
        self._oled.text(message[:16], 0, 36)
        self._oled.show()

    def show_status(self, message: str) -> None:
        if not self._available:
            return
        self._oled.fill(0)
        self._oled.text(message[:16], 0, 28)
        self._oled.show()

    def clear(self) -> None:
        if not self._available:
            return
        self._oled.fill(0)
        self._oled.show()

