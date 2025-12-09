import asyncio
from abc import ABC, abstractmethod


class ExchangeAbstract(ABC):
    @abstractmethod
    async def update_prices(self):
        pass

    @abstractmethod
    async def update_info(self):
        pass

    def update_coins(self):
        with asyncio.TaskGroup as tg:
            asyncio.create_task(self.update_info())
            asyncio.create_task(self.update_prices())