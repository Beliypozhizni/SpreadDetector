import asyncio

from src.coins.aggregator import CoinAggregator
from src.exchanges.exchanges.bitget import BitgetClient
from src.exchanges.exchanges.kucoin import KuCoinClient
from src.utils.logger import logger


class ExchangeManager:
    def __init__(self, coin_aggregator: CoinAggregator):
        self.coin_aggregator = coin_aggregator
        self.update_interval = 5

        self.exchanges = {
            KuCoinClient.name(): KuCoinClient(),
            BitgetClient.name(): BitgetClient(),
        }

        self._stop_event = asyncio.Event()
        self._task: asyncio.Task | None = None

    def start(self) -> None:
        self._stop_event.clear()
        self._task = asyncio.create_task(self._run_loop())

    async def stop(self) -> None:
        self._stop_event.set()
        if self._task:
            await self._task

    async def _run_loop(self):
        while not self._stop_event.is_set():
            await self._update_once()

            try:
                await asyncio.wait_for(
                    self._stop_event.wait(),
                    timeout=self.update_interval,
                )
            except asyncio.TimeoutError:
                pass

    async def _update_once(self):
        async def _safe_update(exchange):
            try:
                return await asyncio.wait_for(
                    exchange.update_coins(),
                    timeout=10,
                )
            except Exception as e:
                logger.error(f"{exchange.name()} update error: {e}")
                return None

        tasks: dict[str, asyncio.Task] = {}

        async with asyncio.TaskGroup() as tg:
            for exchange in self.exchanges.values():
                tasks[exchange.name()] = tg.create_task(_safe_update(exchange))

        for name, task in tasks.items():
            result = task.result()
            if result:
                await self.coin_aggregator.add_coins(
                    coins_data=result,
                    exchange=name,
                )
