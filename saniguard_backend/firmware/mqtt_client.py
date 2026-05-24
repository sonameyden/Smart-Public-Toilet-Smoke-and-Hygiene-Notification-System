"""
MQTT client wrapper for Pico W using umqtt.simple.
"""
import json
import time
import gc
import ssl
import sys
sys.modules['ussl'] = ssl  # register ssl as ussl for umqtt.simple compatibility
from umqtt.simple import MQTTClient
import config


class MQTTPublisher:

    def __init__(self):
        self._client      = None
        self._buffer      = []
        self._connected   = False
        self._last_fail_t = 0

    def connect(self) -> bool:
        now = time.time()
        if self._last_fail_t and (now - self._last_fail_t) < config.MQTT_RECONNECT_COOLDOWN:
            return False

        # Aggressively free memory before TLS allocation
        self._client = None
        gc.collect()
        gc.collect()  # run twice — MicroPython GC sometimes needs two passes
        free = gc.mem_free()
        print("[MQTT] Free RAM before connect: {}KB".format(free // 1024))

        if free < 60000:  # TLS needs ~60KB minimum
            print("[MQTT] Not enough RAM for TLS ({} bytes free). Skipping.".format(free))
            self._last_fail_t = time.time()
            return False

        try:
            self._client = MQTTClient(
                client_id  = config.MQTT_CLIENT_ID,
                server     = config.MQTT_BROKER,
                port       = config.MQTT_PORT,
                user       = config.MQTT_USERNAME,
                password   = config.MQTT_PASSWORD,
                keepalive  = 60,
                ssl        = True,
                ssl_params = {"server_hostname": config.MQTT_BROKER},
            )
            self._client.connect()
            self._connected   = True
            self._last_fail_t = 0
            print("[MQTT] Connected. Free RAM after: {}KB".format(gc.mem_free() // 1024))
            self._flush_buffer()
            return True

        except MemoryError:
            print("[MQTT] ENOMEM — free RAM: {}KB".format(gc.mem_free() // 1024))
            self._client      = None
            self._connected   = False
            self._last_fail_t = time.time()
            gc.collect()
            return False

        except Exception as e:
            print("[MQTT] Connection failed:", e)
            self._client      = None
            self._connected   = False
            self._last_fail_t = time.time()
            return False

    def publish(self, topic: str, payload: dict) -> bool:
        msg = json.dumps(payload)

        if not self._connected:
            self._buffer_message(topic, payload)
            self.connect()
            return False

        try:
            self._client.publish(topic.encode(), msg.encode())
            return True

        except Exception as e:
            print("[MQTT] Publish failed:", e)
            self._connected = False
            self._client    = None
            gc.collect()
            self._buffer_message(topic, payload)
            self.connect()
            return False

    def _buffer_message(self, topic: str, payload: dict) -> None:
        if len(self._buffer) >= config.MAX_BUFFER_SIZE:
            self._buffer.pop(0)
        self._buffer.append((topic, payload))
        print("[MQTT] Buffered ({}/{})".format(len(self._buffer), config.MAX_BUFFER_SIZE))

    def _flush_buffer(self) -> None:
        if not self._buffer:
            return
        print("[MQTT] Flushing {} buffered message(s)".format(len(self._buffer)))
        flushed = []
        for topic, payload in self._buffer:
            try:
                self._client.publish(topic.encode(), json.dumps(payload).encode())
                flushed.append((topic, payload))
            except Exception as e:
                print("[MQTT] Flush error:", e)
                break
        for item in flushed:
            self._buffer.remove(item)

    def disconnect(self) -> None:
        if self._client:
            try:
                self._client.disconnect()
            except Exception:
                pass
        self._connected = False
        self._client    = None