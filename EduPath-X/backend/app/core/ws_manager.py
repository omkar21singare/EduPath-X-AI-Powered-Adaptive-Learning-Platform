from typing import List, Dict, Any
from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        # Maps learner_id to list of active WebSockets
        self.active_connections: Dict[int, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, learner_id: int):
        await websocket.accept()
        if learner_id not in self.active_connections:
            self.active_connections[learner_id] = []
        self.active_connections[learner_id].append(websocket)

    def disconnect(self, websocket: WebSocket, learner_id: int):
        if learner_id in self.active_connections:
            if websocket in self.active_connections[learner_id]:
                self.active_connections[learner_id].remove(websocket)
            if not self.active_connections[learner_id]:
                del self.active_connections[learner_id]

    async def broadcast_to_learner(self, learner_id: int, message: Dict[str, Any]):
        if learner_id in self.active_connections:
            stale = []
            for connection in self.active_connections[learner_id]:
                try:
                    await connection.send_json(message)
                except Exception:
                    stale.append(connection)
            for c in stale:
                self.disconnect(c, learner_id)

    async def broadcast_all(self, message: Dict[str, Any]):
        for learner_id in list(self.active_connections.keys()):
            await self.broadcast_to_learner(learner_id, message)

manager = ConnectionManager()
