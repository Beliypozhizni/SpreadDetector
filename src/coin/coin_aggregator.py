from src.coin.coin_info import CoinInfo


class CoinAggregator:
    def __init__(self):
        self.coins: dict[str, dict[str, CoinInfo]] = {}