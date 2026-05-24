import asyncio
import json
import logging
import ssl

from app.core.config import settings
from app.core.mqtt import SUBSCRIBE_WILDCARD, TOPIC_STATUS
from app.services.sensor_service import process_mqtt_reading
import aiomqtt

logger = logging.getLogger(__name__)


async def start_mqtt_listener() -> None:

    while True:
        try:
            async with aiomqtt.Client(
                hostname=settings.mqtt_broker_host,
                port=settings.mqtt_broker_port,
                username=settings.mqtt_username or None,
                password=settings.mqtt_password or None,
                tls_context=ssl.create_default_context(),
            ) as client:
                logger.info(
                    f"MQTT connected to {settings.mqtt_broker_host}:{settings.mqtt_broker_port}"
                )
                await client.subscribe(SUBSCRIBE_WILDCARD, qos=1)

                async for message in client.messages:
                    topic = str(message.topic)
                    try:
                        payload_data = message.payload
                        if isinstance(payload_data, bytes):
                            payload_data = payload_data.decode()
                        if not isinstance(payload_data, str):
                            logger.warning(f"Non-string payload on {topic}: {payload_data}")
                            continue
                        payload = json.loads(payload_data)
                        await _dispatch(topic, payload)
                    except json.JSONDecodeError:
                        logger.warning(f"Non-JSON payload on {topic}: {message.payload}")
                    except Exception as exc:
                        logger.error(f"Error processing MQTT message on {topic}: {exc}")

        except asyncio.CancelledError:
            logger.info("MQTT listener cancelled — shutting down.")
            break
        except Exception as exc:
            logger.error(f"MQTT connection error: {exc}. Reconnecting in 5s...")
            await asyncio.sleep(5)


async def _dispatch(topic: str, payload: dict) -> None:
    if topic == TOPIC_STATUS:
        return
    if topic.startswith("toilet/sensors/"):
        # process_mqtt_reading is now async — await it so errors surface
        # in this coroutine rather than being silently swallowed by a fire-
        # and-forget task. The Supabase write inside it runs as its own
        # background task, so awaiting here does NOT block the MQTT loop.
        await process_mqtt_reading(topic, payload)
        return
    logger.debug(f"Unhandled MQTT topic: {topic}")