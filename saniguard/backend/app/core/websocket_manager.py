import asyncio
import json
from typing import Any

from fastapi import WebSocket


class WebSocketManager:
    """
    Keeps track of all active WebSocket connections.
    Services call broadcast() to push real-time updates to all connected dashboards.
    """

    def __init__(self):
        self._connections: list[WebSocket] = []

    async def connect(self, ws: WebSocket) -> None:
        await ws.accept()
        self._connections.append(ws)

    def disconnect(self, ws: WebSocket) -> None:
        if ws in self._connections:
            self._connections.remove(ws)

    async def broadcast(self, event_type: str, data: Any) -> None:
        """Send a JSON event to every connected client."""
        if not self._connections:
            return
        payload = json.dumps({"type": event_type, "data": data})
        dead: list[WebSocket] = []
        for ws in self._connections:
            try:
                await ws.send_text(payload)
            except Exception:
                dead.append(ws)
        for ws in dead:
            self.disconnect(ws)

    @property
    def active_count(self) -> int:
        return len(self._connections)


# Singleton — imported by services and the websocket router
ws_manager = WebSocketManager()
