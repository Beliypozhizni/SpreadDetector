import asyncio

from src.coins.aggregator import CoinAggregator
from src.exchanges.base import ExchangeAbstract
from src.exchanges.bitget import BitgetClient
from src.exchanges.kucoin import KuCoinClient
from src.utils.logger import logger


class ExchangeManager:
    def __init__(self, coin_aggregator: CoinAggregator):
        self.is_working = False
        self.update_interval = 5
        self.coin_aggregator = coin_aggregator
        self.exchanges = self._init_exchanges()

    def _init_exchanges(self) -> dict[str, ExchangeAbstract]:
        exchanges = {
            KuCoinClient.name(): KuCoinClient(),
            BitgetClient.name(): BitgetClient(),
        }
        return exchanges

    async def run(self):
        self.is_working = True
        await self._update_data()

    def stop(self):
        self.is_working = False

    async def _update_data(self):
        while self.is_working:
            tasks: dict[str, asyncio.Task] = {}

            try:
                async with asyncio.TaskGroup() as tg:
                    for exchange in self.exchanges.values():
                        tasks[exchange.name()] = tg.create_task(exchange.update_coins())

            except ExceptionGroup as eg:
                for exc in eg.exceptions:
                    logger.error(exc)
                continue

            for exchange_name, task in tasks.items():
                try:
                    result = task.result()
                    if result:
                        self.coin_aggregator.add_coins(
                            coins_data=result,
                            exchange=exchange_name
                        )
                except Exception as e:
                    logger.error(f"Error processing result {exchange_name}: {e}")

            await asyncio.sleep(self.update_interval)
