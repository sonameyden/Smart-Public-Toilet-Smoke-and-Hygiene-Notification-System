import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.exceptions import register_exception_handlers
from app.routers import auth, sensors, alerts, maintenance, analytics, users, activity_logs
from app.routers import settings as settings_router
from app.routers import websocket

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(name)s — %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # ── Startup ──────────────────────────────────────────────────────────────
    logger.info("Starting Saniguard API...")
    from app.services.mqtt_listener import start_mqtt_listener
    mqtt_task = asyncio.create_task(start_mqtt_listener())
    logger.info("MQTT listener task started")

    yield

    # ── Shutdown ─────────────────────────────────────────────────────────────
    logger.info("Shutting down Saniguard API...")
    mqtt_task.cancel()
    try:
        await mqtt_task
    except asyncio.CancelledError:
        pass


def create_app() -> FastAPI:
    app = FastAPI(
        title="Saniguard API",
        description="Smart Public Toilet Smoke & Hygiene Monitoring System",
        version="1.0.0",
        lifespan=lifespan,
    )

    # CORS — allow the React dev server and any configured origins
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Global exception handlers
    register_exception_handlers(app)

    # Routers — all prefixed under /api/v1
    prefix = "/api/v1"
    app.include_router(auth.router,             prefix=prefix)
    app.include_router(sensors.router,          prefix=prefix)
    app.include_router(alerts.router,           prefix=prefix)
    app.include_router(maintenance.router,      prefix=prefix)
    app.include_router(analytics.router,        prefix=prefix)
    app.include_router(users.router,            prefix=prefix)
    app.include_router(settings_router.router,  prefix=prefix)
    app.include_router(activity_logs.router,    prefix=prefix)
    app.include_router(websocket.router,        prefix=prefix)

    @app.get("/health", tags=["health"])
    def health():
        return {"status": "ok", "service": "saniguard-api"}

    return app


app = create_app()
