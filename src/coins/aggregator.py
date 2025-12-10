from src.coins.data import CoinData
from src.utils.logger import logger


class CoinAggregator:
    def __init__(self):
        self.coins: dict[str, dict[str, CoinData]] = {}

    def add_coins(self, coins_data: list[CoinData], exchange: str):
        for data in coins_data:
            chain = data.coin_info.chain
            contract = data.coin_info.contract
            if chain is None or contract is None:
                logger.warning(f"chain or contract not found in data")
                continue
            key = data.coin_info.chain + data.coin_info.contract
            self.coins.setdefault(key, {})[exchange] = data
        return None

    def get_coins(self):
        return self.coins.copy()
