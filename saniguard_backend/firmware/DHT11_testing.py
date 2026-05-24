from machine import Pin
import dht
import time

sensor = dht.DHT11(Pin(14, Pin.OUT, Pin.PULL_DOWN))

time.sleep(2)  # warm up

for _ in range(5):
    try:
        sensor.measure()
        print("Temp:", sensor.temperature(), "C")
        print("Humidity:", sensor.humidity(), "%")
    except Exception as e:
        print("Error:", e)
    time.sleep(2)
