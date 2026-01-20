from typing import Callable

from src.chains.mapper import ChainsMapper
from src.coins.data import CoinData
from src.utils.logger import logger


class CoinAggregator:
    def __init__(self, chains_mapper: ChainsMapper):
        self.chains_mapper = chains_mapper
        self.coins: dict[str, dict[str, CoinData]] = {}
        self._on_coins_added_callbacks: list[Callable] = []
        print('Coin Aggregator initialized')

    def on_coins_added(self, callback: Callable):
        self._on_coins_added_callbacks.append(callback)

    async def add_coins(self, coins_data: list[CoinData], exchange: str):
        for data in coins_data:
            chain = self.chains_mapper.resolve(data.coin_info.chain)
            contract = data.coin_info.contract
            if chain is None or contract is None:
                logger.warning(f"chain or contract not found in data")
                continue
            key = data.coin_info.chain + data.coin_info.contract
            self.coins.setdefault(key, {})[exchange] = data

        for callback in self._on_coins_added_callbacks:
            try:
                await callback()
            except Exception as e:
                logger.error(f"Error in coins added callback: {e}")

        return None

    def get_coins(self):
        return self.coins.copy()
