from __future__ import annotations

import asyncio
from typing import Awaitable, Callable

from src.spreads.spread import Spread
from src.utils.logger import logger

SpreadsCallback = Callable[[list[Spread]], Awaitable[None]]


class SpreadStorage:
    def __init__(self):
        self._spreads: list[Spread] = []
        self._callbacks: list[SpreadsCallback] = []
        self._lock = asyncio.Lock()

    def on_spreads_updated(self, callback: SpreadsCallback) -> None:
        self._callbacks.append(callback)

    async def set_spreads(self, spreads: list[Spread]) -> None:
        async with self._lock:
            self._spreads = spreads
            spreads_snapshot = spreads.copy()
            callbacks_snapshot = self._callbacks.copy()

        async def _safe(cb: SpreadsCallback):
            try:
                await cb(spreads_snapshot)
            except Exception as e:
                logger.error(f"Error in spreads updated callback: {e}")

        await asyncio.gather(
            *(_safe(cb) for cb in callbacks_snapshot),
            return_exceptions=True,
        )

    async def get_spreads(self) -> list[Spread]:
        async with self._lock:
            return self._spreads.copy()

    async def get_spreads_json(self) -> list[dict]:
        spreads = await self.get_spreads()
        return [s.to_json for s in spreads]
