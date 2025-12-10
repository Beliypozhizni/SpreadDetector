from dataclasses import dataclass
from src.coins.info import CoinInfo
from src.coins.prices import CoinPrices


@dataclass
class CoinData:
    coin_prices: CoinPrices
    coin_info: CoinInfo
