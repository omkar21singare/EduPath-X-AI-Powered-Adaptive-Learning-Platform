import logging
from typing import Dict, Any
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.core.ws_manager import manager

logger = logging.getLogger(__name__)
router = APIRouter(tags=["WebSockets"])

@router.websocket("/ws/{learner_id}")
async def websocket_realtime_endpoint(websocket: WebSocket, learner_id: int):
    await manager.connect(websocket, learner_id)
    try:
        # Send initial confirmation
        await websocket.send_json({
            "event": "CONNECTED",
            "learner_id": learner_id,
            "message": "Real-time EduPath-X WebSocket channel open."
        })
        while True:
            data = await websocket.receive_text()
            if data == "ping":
                await websocket.send_text("pong")
    except WebSocketDisconnect:
        manager.disconnect(websocket, learner_id)
    except Exception as e:
        logger.debug(f"WebSocket closed: {e}")
        manager.disconnect(websocket, learner_id)
