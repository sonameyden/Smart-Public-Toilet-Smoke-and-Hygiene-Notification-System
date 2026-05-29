# Saniguard — Smart Public Toilet Smoke & Hygiene Monitoring

This repository implements a full-stack IoT system for smoke/gas and hygiene monitoring in public toilets. It includes:

- A React frontend (dashboard and management UI).
- A FastAPI backend that exposes a REST/WebSocket API and listens to MQTT messages.
- MicroPython firmware for a Raspberry Pi Pico W that reads sensors and publishes MQTT messages.
- An MQTT broker service (Eclipse Mosquitto) in `docker-compose.yml` for local integration and testing.

This project was developed as part of the IoT module mini-project at the College of Science and Technology, Royal University of Bhutan. I am grateful to my instructors, classmates, and everyone who supported this work.

This single README summarizes the codebase, high-level architecture, how components connect, and how to run the entire stack locally.

**Repository layout**

- `frontend/` — React + Vite app
- `saniguard_backend/`
  - `docker-compose.yml` — launches Mosquitto and the backend API
  - `backend/` — FastAPI application
  - `firmware/` — MicroPython firmware for Pico W

**High-level architecture & workflow**

1. Firmware on the Pico W reads sensors (MQ-2, MQ-135, DHT) periodically and publishes readings to MQTT topics (e.g. `toilet/sensors/smoke`).
2. Mosquitto receives sensor messages and the backend (FastAPI) subscribes via an async MQTT listener. The listener parses messages and updates caches, triggers alerts, and persists activity/data (supabase or other configured store).
3. The frontend (React) calls the backend REST API under `/api/v1` for dashboard data, user management, and settings. The frontend also uses a WebSocket endpoint exposed by the backend to receive live updates.

Components

- Frontend (frontend/)
  - Entry: `src/main.jsx` — wraps the app with React Query.
  - Routing: `src/App.jsx` -> lazy loads feature pages (auth, dashboard, alerts, analytics, maintenance, users, settings).
  - API client: `src/lib/api-client.js` — axios instance with base URL `/api/v1` and JWT interceptor.

- Backend (saniguard_backend/backend/)
  - Entry: `app/main.py` — FastAPI app factory, lifespan manager that starts an MQTT listener task and includes routers under `/api/v1`.
  - Config: `app/core/config.py` — pydantic-based settings read from `.env` (supabase keys, JWT settings, MQTT broker host/port, CORS origins).
  - MQTT listener: runs on startup via `app.services.mqtt_listener.start_mqtt_listener()` (task created in `lifespan`).
  - Routers: `app.routers.*` (auth, sensors, alerts, maintenance, analytics, users, activity_logs, websocket).

- Firmware (saniguard_backend/firmware/)
  - Entry: `main.py` — connects to Wi‑Fi, initializes sensors, updates local OLED, publishes sensor readings to MQTT topics, and triggers local alerts (buzzer/LED/OLED) on thresholds.
  - Config: `config.py` — Wi‑Fi, MQTT broker credentials, topics, GPIO pin assignments, thresholds, and read interval.

MQTT topics (firmware ↔ backend)

- `toilet/sensors/smoke` — MQ-2 smoke ppm
- `toilet/sensors/gas` — MQ-135 gas ppm
- `toilet/sensors/air_quality` — computed air quality score
- `toilet/sensors/env` — temperature & humidity JSON
- `toilet/status` — optional device status/heartbeat

Configuration & environment

Backend uses `pydantic-settings` and an `.env` file. Key variables expected (example):

```
SUPABASE_URL=https://your.supabase.instance
SUPABASE_KEY=your-service-role-or-anon-key
JWT_SECRET_KEY=very-secret-value
# MQTT broker used by backend if subscribing directly (overrides compose broker if needed)
MQTT_BROKER_HOST=localhost
MQTT_BROKER_PORT=1883
MQTT_USERNAME=
MQTT_PASSWORD=
CORS_ORIGINS=http://localhost:5173
```

Firmware configuration lives in `saniguard_backend/firmware/config.py` and contains Wi‑Fi and MQTT credentials. Update these values before flashing your Pico W.

How to run everything (recommended: Docker Compose)

1. From the repository root, start the MQTT broker and backend API with Docker Compose:

```bash
cd saniguard_backend
docker-compose up --build
```

This will:
- Start a Mosquitto broker on host port `1883` (container `saniguard-mqtt`).
- Build and run the backend API on port `8000` (container `saniguard-api`).

2. Confirm backend health (after containers are running):

```bash
curl http://localhost:8000/health
# expected JSON: {"status":"ok","service":"saniguard-api"}
```

3. Run the frontend (dev server) locally:

```bash
cd frontend
npm install
npm run dev
```

Open the browser at the Vite dev URL (typically `http://localhost:5173`). The frontend makes API calls to `/api/v1` — when using Docker Compose, you may want to proxy dev server requests to the backend. The frontend's axios baseURL is `/api/v1`, so if running dev server separately set up a dev proxy or use the backend host directly in production build.

Running the backend locally (without Docker)

```bash
cd saniguard_backend/backend
python -m venv .venv
.venv\\Scripts\\activate      # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Flashing firmware to Raspberry Pi Pico W (MicroPython)

1. Install MicroPython firmware for the Pico W (use Thonny or the Raspberry Pi official instructions).
2. Update `saniguard_backend/firmware/config.py` with your Wi‑Fi and MQTT credentials and desired thresholds.
3. Copy the firmware files to the Pico W filesystem (Thonny, rshell, or ampy). Ensure `main.py` and the `sensors/`, `mqtt_client.py`, `display.py`, `alert.py`, and `config.py` are present on the device.

Quick flashing example with Thonny:

```
# In Thonny, open the firmware folder and save each .py file to the device.
# Reboot the Pico W; `main.py` runs automatically.
```

Notes on security & secrets

- The firmware `config.py` contains plain text Wi‑Fi and broker credentials. Keep access to the firmware folder secure.
- The backend `.env` should never be committed; add it to `.gitignore` (there's a repo-level `.gitignore` already in this workspace).
- For production use, run Mosquitto with TLS and use strong credentials; rotate JWT and Supabase keys.

Development and testing

- Backend tests use `pytest`; see `saniguard_backend/backend/pyproject.toml` test config. Run tests from the backend folder:

```
cd saniguard_backend/backend
pytest
```

Where to look in the code

- Frontend routes and pages: `frontend/src/features/*/pages`
- API client: `frontend/src/lib/api-client.js`
- Backend app startup & lifecycles: `saniguard_backend/backend/app/main.py`
- Backend settings: `saniguard_backend/backend/app/core/config.py`
- Firmware main loop: `saniguard_backend/firmware/main.py`
- Firmware configuration: `saniguard_backend/firmware/config.py`

Troubleshooting

- If the backend fails to connect to the MQTT broker, ensure `mosquitto` is up and reachable at the configured host/port and credentials match.
- If the frontend shows authentication redirects, ensure the backend's JWT secret and user system are configured and that the frontend is pointed at the correct backend URL.
- When flashing the Pico W, if sensors read `None` for DHT values, check wiring and `DHT_MODEL` in `config.py`.

Next steps I can help with

- Add a `.env.example` file for the backend with required keys.
- Add a `docker-compose.frontend.yml` to host the frontend inside Docker for an end-to-end `docker-compose up` experience.
- Create short HOWTO scripts for flashing the Pico W via command line tools.
