# ─────────────────────────────────────────────────────────────────────────────
# Saniguard Firmware Configuration
# Edit this file before flashing to your Raspberry Pi Pico W.
# ─────────────────────────────────────────────────────────────────────────────

# Wi-Fi credentials
WIFI_SSID     = "SE"
WIFI_PASSWORD = "sonameyden1000"

# MQTT broker
MQTT_BROKER    = "246a8c54fc6e407a82225dc180715c65.s1.eu.hivemq.cloud"
MQTT_PORT      = 8883
MQTT_CLIENT_ID = "saniguard-pico-01"
MQTT_USERNAME  = "SonamEyden"
MQTT_PASSWORD  = "Sonam20052025#"

# MQTT topics (must match backend/app/core/mqtt.py)
TOPIC_SMOKE       = "toilet/sensors/smoke"
TOPIC_GAS         = "toilet/sensors/gas"
TOPIC_AIR_QUALITY = "toilet/sensors/air_quality"
TOPIC_ENV         = "toilet/sensors/env"
TOPIC_STATUS      = "toilet/status"

# GPIO pin assignments (Raspberry Pi Pico W)
PIN_MQ2_ADC   = 26   # GP26 = ADC0 — MQ-2 smoke sensor
PIN_MQ135_ADC = 27   # GP27 = ADC1 — MQ-135 gas sensor
PIN_DHT       = 14   # GP14 — DHT11/DHT22 temperature & humidity
PIN_BUZZER    = 15   # GP15 — buzzer PWM
PIN_LED_RED   = 16   # GP16 — red alert LED
PIN_LED_GREEN = 17   # GP17 — green status LED
PIN_SDA       = 4    # GP4  — OLED I2C SDA
PIN_SCL       = 5    # GP5  — OLED I2C SCL

# DHT sensor model — set to "DHT11" or "DHT22" to match your physical sensor
DHT_MODEL = "DHT11"

# Read interval (seconds)
READ_INTERVAL = 3

# Local thresholds — trigger buzzer/LED immediately
SMOKE_THRESHOLD       = 30.0
GAS_THRESHOLD         = 100.0
AIR_QUALITY_THRESHOLD = 70.0

# MQ sensor R0 calibration constants
MQ2_R0   = 9.83
MQ135_R0 = 3.68

# OLED
OLED_WIDTH  = 128
OLED_HEIGHT = 64

# Offline buffer size — keep small to avoid RAM pressure
MAX_BUFFER_SIZE = 10

# MQTT reconnect cooldown (seconds) — prevents rapid retry ENOMEM loop
MQTT_RECONNECT_COOLDOWN = 30
