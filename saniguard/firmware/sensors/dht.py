"""
DHT11 / DHT22 Temperature & Humidity Sensor Driver wrapper for Pico W.
Uses MicroPython's built-in dht module.
"""
import dht
import time
from machine import Pin


class DHTSensor:
    """
    Wiring:
        VCC  -> 3.3V
        GND  -> GND
        DATA -> any GPIO (e.g. GP14)

    Note: a 10kΩ pull-up resistor between DATA and 3.3V is strongly recommended.
    If you don't have one, the internal pull-up (Pin.PULL_UP) below acts as a
    fallback and usually resolves ETIMEDOUT errors.
    """

    def __init__(self, pin: int, model: str = "DHT11"):
        gpio = Pin(pin, Pin.OUT, Pin.PULL_DOWN)
        self._sensor = dht.DHT11(gpio) if model == "DHT11" else dht.DHT22(gpio)
        print("[DHT] Warming up sensor...")
        time.sleep_ms(2000)  # 2 second warm-up after power on
        print("[DHT] Ready")

    def read(self) -> dict:
        """
        Returns {"temperature": float, "humidity": float} or
        {"temperature": None, "humidity": None} on error.
        Retries up to 3 times before giving up.
        """
        for attempt in range(3):
            try:
                time.sleep_ms(500)  # stabilisation delay before each measure
                self._sensor.measure()
                return {
                    "temperature": self._sensor.temperature(),
                    "humidity":    self._sensor.humidity(),
                }
            except Exception as e:
                print("DHT read error (attempt {}/3): {}".format(attempt + 1, e))
                time.sleep_ms(1000)  # wait before retrying

        return {"temperature": None, "humidity": None}
