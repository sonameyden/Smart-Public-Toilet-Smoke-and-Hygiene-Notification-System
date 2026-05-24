import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.core.websocket_manager import ws_manager
from app.core.security import decode_access_token
from app.services.sensor_service import get_latest

router = APIRouter(tags=["websocket"])


@router.websocket("/ws/dashboard")
async def dashboard_ws(websocket: WebSocket):
    """
    Real-time dashboard WebSocket.
    Clients must send a valid JWT as the first text message after connecting.
    Once authenticated, they receive:
      - sensor_update   → every new MQTT sensor reading
      - new_alert       → when a new alert is created
      - alert_resolved  → when an alert is resolved
    """
    await ws_manager.connect(websocket)
    try:
        # Step 1: wait for the auth token
        raw = await websocket.receive_text()
        payload = decode_access_token(raw.strip())
        if not payload:
            await websocket.send_text(
                json.dumps({"type": "error", "data": "Invalid token"})
            )
            await websocket.close(code=4001)
            ws_manager.disconnect(websocket)
            return

        # Step 2: send the current sensor snapshot immediately on connect
        latest = get_latest()
        if latest:
            await websocket.send_text(
                json.dumps({
                    "type": "sensor_update",
                    "data": latest.model_dump(mode="json"),
                })
            )

        # Step 3: keep the connection alive; client can send pings
        while True:
            msg = await websocket.receive_text()
            if msg == "ping":
                await websocket.send_text(json.dumps({"type": "pong"}))

    except WebSocketDisconnect:
        pass
    finally:
        ws_manager.disconnect(websocket)
