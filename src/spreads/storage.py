from typing import Callable

from src.spreads.spread import Spread
from src.utils.logger import logger


class SpreadStorage:
    def __init__(self):
        self._spreads: list[Spread] = []
        self._on_spreads_updated_callbacks: list[Callable] = []

    def on_spreads_updated(self, callback: Callable):
        self._on_spreads_updated_callbacks.append(callback)

    async def add_spreads(self, spreads: list[Spread]):
        self._spreads = spreads

        for callback in self._on_spreads_updated_callbacks:
            try:
                await callback()
            except Exception as e:
                logger.error(f"Error in spreads updated callback: {e}")

    def get_spreads(self):
        return self._spreads.copy()

    def get_spreads_json(self):
        spreads_json = []
        for spread in self._spreads:
            spreads_json.append(spread.to_json)
        return spreads_json
