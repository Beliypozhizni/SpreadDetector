import asyncio

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends

from src.spreads.storage import SpreadStorage

router = APIRouter(prefix="/spreads", tags=["Spreads"])


def get_spread_storage_ws(ws: WebSocket) -> SpreadStorage:
    return ws.app.state.spread_storage


class ConnectionManager:
    def __init__(self):
        self._connections: set[WebSocket] = set()
        self._lock = asyncio.Lock()

    async def connect(self, ws: WebSocket):
        await ws.accept()
        async with self._lock:
            self._connections.add(ws)

    async def disconnect(self, ws: WebSocket):
        async with self._lock:
            self._connections.discard(ws)

    async def broadcast(self, message: list[dict]):
        async with self._lock:
            conns = list(self._connections)

        if not conns:
            return

        async def _safe_send(ws: WebSocket):
            try:
                await ws.send_json(message)
            except Exception:
                await self.disconnect(ws)

        await asyncio.gather(
            *(_safe_send(ws) for ws in conns),
            return_exceptions=True,
        )


manager = ConnectionManager()


@router.on_event("startup")
async def register_storage_callback():
    async def _callback(spreads):
        await manager.broadcast([s.to_json for s in spreads])

    async def _bind(app):
        storage: SpreadStorage = app.state.spread_storage
        storage.on_spreads_updated(_callback)

    router._bind_callback = _bind


@router.websocket("/")
async def websocket_endpoint(
        websocket: WebSocket,
        storage: SpreadStorage = Depends(get_spread_storage_ws),
):
    if hasattr(router, "_bind_callback"):
        await router._bind_callback(websocket.app)
        delattr(router, "_bind_callback")

    await manager.connect(websocket)

    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        await manager.disconnect(websocket)
