"""
Saniguard Firmware — main entry point for Raspberry Pi Pico W.
MicroPython entry point: this file runs automatically on boot.

Flow:
  1. Connect to Wi-Fi
  2. Init sensors, buzzer, LED, OLED
  3. Connect to MQTT broker
  4. Loop every READ_INTERVAL seconds:
       a. Read all sensors
       b. Check thresholds → fire local alert if needed
       c. Update OLED display
       d. Publish readings to MQTT
"""
import time
import network
import json

import config
from sensors.mq2    import MQ2
from sensors.mq135  import MQ135
from sensors.dht    import DHTSensor
from mqtt_client    import MQTTPublisher
from alert          import LocalAlert
from display        import OLEDDisplay


# ── Wi-Fi connection ─────────────────────────────────────────────────────────

def connect_wifi() -> bool:
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if wlan.isconnected():
        return True

    print("[WiFi] Connecting to", config.WIFI_SSID, "...")
    wlan.connect(config.WIFI_SSID, config.WIFI_PASSWORD)

    for _ in range(20):                   # wait up to 10 seconds
        if wlan.isconnected():
            print("[WiFi] Connected. IP:", wlan.ifconfig()[0])
            return True
        time.sleep(0.5)

    print("[WiFi] Connection failed")
    return False


# ── Bootstrap ────────────────────────────────────────────────────────────────

def main():
    # Hardware init
    mq2     = MQ2(config.PIN_MQ2_ADC,     r0=config.MQ2_R0)
    mq135   = MQ135(config.PIN_MQ135_ADC, r0=config.MQ135_R0)
    dht     = DHTSensor(pin=config.PIN_DHT, model=config.DHT_MODEL)
    alerter = LocalAlert(config.PIN_BUZZER, config.PIN_LED_RED, config.PIN_LED_GREEN)
    display = OLEDDisplay(config.PIN_SDA, config.PIN_SCL, config.OLED_WIDTH, config.OLED_HEIGHT)
    mqtt    = MQTTPublisher()

    display.show_status("Booting...")

    # MQ sensor warm-up — must stabilise before readings are trusted
    print("[Main] Warming up MQ sensors (2 min)...")
    display.show_status("Warming up...")
    time.sleep(120)

    # Connect Wi-Fi
    wifi_ok = connect_wifi()
    if not wifi_ok:
        display.show_status("WiFi failed")
        # Continue without Wi-Fi — local alerts still work

    # Connect MQTT
    mqtt.connect()
    display.show_status("Ready")
    time.sleep(1)

    print("[Main] Starting sensor loop (interval={}s)".format(config.READ_INTERVAL))

    # ── Main loop ────────────────────────────────────────────────────────────
    while True:
        try:
            # 1. Read sensors
            smoke_ppm   = mq2.read_ppm()
            gas_ppm     = mq135.read_ppm()
            air_quality = mq135.read_air_quality_score()
            env         = dht.read()

            # Log DHT failures explicitly instead of silently falling back
            temperature = env["temperature"]
            humidity    = env["humidity"]
            if temperature is None or humidity is None:
                print("[Sensor] DHT read failed — check wiring or DHT_MODEL in config.py")
                temperature = temperature if temperature is not None else 25.0
                humidity    = humidity    if humidity    is not None else 50.0

            print("[Sensor] smoke={} gas={} air={} temp={} hum={}".format(
                smoke_ppm, gas_ppm, air_quality, temperature, humidity
            ))

            # 2. Local threshold checks — instant hardware response
            alert_fired = False
            if smoke_ppm > config.SMOKE_THRESHOLD:
                print("[Alert] Smoke detected!")
                alerter.smoke_alert()
                display.show_alert("SMOKE!")
                alert_fired = True
            elif gas_ppm > config.GAS_THRESHOLD:
                print("[Alert] Gas level elevated!")
                alerter.hygiene_warning()
                display.show_alert("GAS!")
                alert_fired = True
            elif air_quality < config.AIR_QUALITY_THRESHOLD:
                print("[Alert] Poor hygiene!")
                alerter.hygiene_warning()
                display.show_alert("HYGIENE!")
                alert_fired = True
            else:
                alerter.clear()

            # 3. Update OLED with live readings (skip if alert is showing)
            if not alert_fired:
                display.show_readings(smoke_ppm, gas_ppm, air_quality, temperature, humidity)

            # 4. Publish each sensor reading as a separate MQTT message
            ts = time.time()

            mqtt.publish(config.TOPIC_SMOKE,       {"ppm": smoke_ppm,     "ts": ts})
            mqtt.publish(config.TOPIC_GAS,         {"ppm": gas_ppm,       "ts": ts})
            mqtt.publish(config.TOPIC_AIR_QUALITY, {"score": air_quality, "ts": ts})
            mqtt.publish(config.TOPIC_ENV, {
                "temp":     temperature,
                "humidity": humidity,
                "ts":       ts,
            })

        except Exception as e:
            print("[Main] Loop error:", e)

        time.sleep(config.READ_INTERVAL)


# ── Entry point ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    main()
