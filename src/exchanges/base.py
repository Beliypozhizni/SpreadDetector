import asyncio
from abc import ABC
from typing import Type, Any

import aiohttp

from src.coins.data import CoinData
from src.coins.info import CoinInfo
from src.coins.prices import CoinPrices
from src.exchanges.configs.abstract import ExchangeConfig, EndpointType
from src.exchanges.parsers.abstract import BaseParser
from src.utils.logger import logger


class ExchangeAbstract(ABC):
    TIMEOUT = aiohttp.ClientTimeout(total=30)
    CONFIG_CLASS: Type[ExchangeConfig]
    PARSER_CLASS: Type[BaseParser]

    def __init__(self):
        self.config = self.CONFIG_CLASS
        self.parser = self.PARSER_CLASS(self.config)

    @classmethod
    def name(cls) -> str:
        """Название биржи"""
        return cls.CONFIG_CLASS.name

    @property
    def base_url(self) -> str:
        """URL API биржи"""
        return self.config.base_url

    @property
    def timeout(self) -> int:
        return 10

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
            logger.error(f"{self.name()}: Ошибки в задачах: {len(eg.exceptions)}, {eg}")
            return []
        except Exception as e:
            logger.error(f"{self.name()}: Ошибка в update_coins: {e}")
            return []

    async def _make_request(self, endpoint: str) -> dict | None:
        return await self.http.get_json(endpoint)

    async def close(self):
        """Корректное закрытие ресурсов"""
        await self.http.close()

    async def get_prices(self) -> dict[str, Any]:
        """Получение цен"""
        endpoint = self.config.endpoints[EndpointType.PRICES]
        data = await self._make_request(endpoint)
        if not data:
            logger.error(f"{self.name()}: Failed to fetch prices")
            return {}
        return self.parser.parse_prices(data)

    async def get_info(self) -> dict[str, list]:
        """Получение информации о монетах"""
        endpoint = self.config.endpoints[EndpointType.INFO]
        data = await self._make_request(endpoint)
        if not data:
            logger.error(f"{self.name()}: Failed to fetch coin info")
            return {}
        return self.parser.parse_info(data)
