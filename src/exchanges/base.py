import asyncio
from abc import ABC, abstractmethod

import aiohttp

from src.coins.data import CoinData
from src.coins.info import CoinInfo
from src.coins.prices import CoinPrices
from src.http_client import HttpClient
from src.utils.logger import logger


class ExchangeAbstract(ABC):
    TIMEOUT = aiohttp.ClientTimeout(total=30)

    @classmethod
    @abstractmethod
    def name(cls) -> str:
        """Название биржи"""
        pass

    @property
    @abstractmethod
    def base_url(self) -> str:
        """URL API биржи"""
        pass

    @property
    def timeout(self) -> int:
        return 10

    def __init__(self):
        self.http = HttpClient(
            base_url=self.base_url,
            timeout=self.timeout
        )

    async def update_coins(self) -> list[CoinData]:
        """Получает все необходимые данные для CoinData и отдает их CoinAggregator"""
        try:
            async with asyncio.TaskGroup() as tg:
                prices_task = tg.create_task(self.get_prices())
                info_task = tg.create_task(self.get_info())

            prices = prices_task.result()
            info = info_task.result()

            if prices is None or info is None:
                logger.error(
                    f"{self.name()}: Не удалось получить данные (prices={prices is not None}, info={info is not None})")
                return []

            aggregated_coins_data = self.aggregate_coins_data(coins_prices=prices, coins_info=info)
            return aggregated_coins_data
        except ExceptionGroup as eg:
            logger.error(f"{self.name()}: Ошибки в задачах: {len(eg.exceptions)}")
            return []
        except Exception as e:
            logger.error(f"{self.name()}: Ошибка в update_coins: {e}")
            return []

    def aggregate_coins_data(self, coins_prices: dict[str, CoinPrices], coins_info: dict[str, list[CoinInfo]]):
        coins_data: list[CoinData] = []
        for name, item in coins_info.items():
            price = coins_prices.get(name)
            info = coins_info.get(name)

            if not price or not info:
                continue

            for inf in info:
                coins_data.append(CoinData(coin_prices=price, coin_info=inf))
        return coins_data

    async def _make_request(self, endpoint: str) -> dict | None:
        return await self.http.get_json(endpoint)

    async def close(self):
        """Корректное закрытие ресурсов"""
        await self.http.close()

    @abstractmethod
    async def get_prices(self) -> dict[str, CoinPrices] | None:
        """Запрашивает ask и bid цены по API биржи"""
        pass

    @abstractmethod
    async def get_info(self) -> dict[str, list[CoinInfo]] | None:
        """Запрашивает сети, адреса, статусы депозита и вывода по API биржи"""
        pass
