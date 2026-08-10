from typing import Any, cast

from fastapi import WebSocket


class ConnectionManager:
    def __init__(self) -> None:
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket) -> None:
        self.active_connections.remove(websocket)

    async def receive_json(self, websocket: WebSocket) -> dict[Any, Any]:
        return cast("dict[Any, Any]", await websocket.receive_json())

    async def send_personal_message(self, data: str, websocket: WebSocket) -> None:
        await websocket.send_text(data)

    async def broadcast(self, message: str) -> None:
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()
